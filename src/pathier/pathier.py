import pathlib
import json
import tomlkit
from typing import Any, Self
import os
import shutil
import functools


class Pathier(pathlib.Path):
    """Subclasses the standard library pathlib.Path class."""

    def __new__(cls, *args, **kwargs):
        if cls is Pathier:
            cls = WindowsPath if os.name == "nt" else PosixPath
        self = cls._from_parts(args)
        if not self._flavour.is_supported:
            raise NotImplementedError(
                "cannot instantiate %r on your system" % (cls.__name__,)
            )
        return self

    def mkdir(self, mode: int = 511, parents: bool = True, exist_ok: bool = True):
        """Create this directory.
        Same as Path().mkdir() except
        'parents' and 'exist_ok' default
        to True instead of False."""
        super().mkdir(mode, parents, exist_ok)

    def write_text(
        self,
        data: Any,
        encoding: Any | None = None,
        errors: Any | None = None,
        newline: Any | None = None,
        parents: bool = True,
    ):
        """Write data to file. If a TypeError is raised, the function
        will attempt to case data to a str and try the write again.
        If a FileNotFoundError is raised and parents = True,
        self.parent will be created."""
        write = functools.partial(
            super().write_text,
            encoding=encoding,
            errors=errors,
            newline=newline,
        )
        try:
            write(data)
        except TypeError:
            data = str(data)
            write(data)
        except FileNotFoundError:
            if parents:
                self.parent.mkdir(parents=True)
                write(data)
            else:
                raise
        except Exception as e:
            raise

    def write_bytes(self, data: bytes, parents: bool = True):
        """Write bytes to file.

        :param parents: If True and the write operation fails
        with a FileNotFoundError, make the parent directory
        and retry the write."""
        try:
            super().write_bytes(data)
        except FileNotFoundError:
            if parents:
                self.parent.mkdir(parents=True)
                super().write_bytes(data)
            else:
                raise
        except Exception as e:
            raise

    def json_loads(self, encoding: Any | None = None, errors: Any | None = None) -> Any:
        """Load json file."""
        return json.loads(self.read_text(encoding, errors))

    def json_dumps(
        self,
        data: Any,
        encoding: Any | None = None,
        errors: Any | None = None,
        newline: Any | None = None,
        sort_keys: bool = False,
        indent: Any | None = None,
        default: Any | None = None,
        parents: bool = True,
    ) -> Any:
        """Dump data to json file."""
        self.write_text(
            json.dumps(data, indent=indent, default=default, sort_keys=sort_keys),
            encoding,
            errors,
            newline,
            parents,
        )

    def toml_loads(self, encoding: Any | None = None, errors: Any | None = None) -> Any:
        """Load toml file."""
        return tomlkit.loads(self.read_text(encoding, errors))

    def toml_dumps(
        self,
        data: Any,
        encoding: Any | None = None,
        errors: Any | None = None,
        newline: Any | None = None,
        sort_keys: bool = False,
        parents: bool = True,
    ):
        """Dump data to toml file."""
        self.write_text(
            tomlkit.dumps(data, sort_keys), encoding, errors, newline, parents
        )

    def loads(self, encoding: Any | None = None, errors: Any | None = None) -> Any:
        """Load a json or toml file based off this instance's suffix."""
        match self.suffix:
            case ".json":
                return self.json_loads(encoding, errors)
            case ".toml":
                return self.toml_loads(encoding, errors)

    def dumps(
        self,
        data: Any,
        encoding: Any | None = None,
        errors: Any | None = None,
        newline: Any | None = None,
        sort_keys: bool = False,
        indent: Any | None = None,
        default: Any | None = None,
        parents: bool = True,
    ):
        """Dump data to a json or toml file based off this instance's suffix."""
        match self.suffix:
            case ".json":
                self.json_dumps(
                    data, encoding, errors, newline, sort_keys, indent, default, parents
                )
            case ".toml":
                self.toml_dumps(data, encoding, errors, newline, sort_keys, parents)

    def delete(self, missing_ok: bool = True):
        """Delete the file or folder pointed to by this instance.
        Uses self.unlink() if a file and uses shutil.rmtree() if a directory."""
        if self.is_file():
            self.unlink(missing_ok)
        elif self.is_dir():
            shutil.rmtree(self)


class PosixPath(Pathier, pathlib.PurePosixPath):
    __slots__ = ()


class WindowsPath(Pathier, pathlib.PureWindowsPath):
    __slots__ = ()
