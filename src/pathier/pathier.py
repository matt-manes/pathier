import datetime
import functools
import json
import os
import pathlib
import shutil
from typing import Any, Self
import sys

import tomlkit


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

    # ===============================================stats===============================================
    @property
    def dob(self) -> datetime.datetime | None:
        """Returns the creation date of this file
        or directory as a dateime.datetime object."""
        if self.exists():
            return datetime.datetime.fromtimestamp(self.stat().st_ctime)
        else:
            return None

    @property
    def age(self) -> float | None:
        """Returns the age in seconds of this file or directory."""
        if self.exists():
            return (datetime.datetime.now() - self.dob).total_seconds()
        else:
            return None

    @property
    def mod_date(self) -> datetime.datetime | None:
        """Returns the modification date of this file
        or directory as a datetime.datetime object."""
        if self.exists():
            return datetime.datetime.fromtimestamp(self.stat().st_mtime)
        else:
            return None

    @property
    def mod_delta(self) -> float | None:
        """Returns how long ago in seconds this file
        or directory was modified."""
        if self.exists():
            return (datetime.datetime.now() - self.mod_date).total_seconds()
        else:
            return None

    def size(self, format: bool = False) -> int | str | None:
        """Returns the size in bytes of this file or directory.
        Returns None if this path doesn't exist.

        :param format: If True, return value as a formatted string."""
        if not self.exists():
            return None
        if self.is_file():
            size = self.stat().st_size
        if self.is_dir():
            size = sum(file.stat().st_size for file in self.rglob("*.*"))
        if format:
            return self.format_size(size)
        return size

    @staticmethod
    def format_size(size: int) -> str:
        """Format 'size' with common file size abbreviations
        and rounded to two decimal places.
        >>> 1234 -> "1.23 kb" """
        for unit in ["bytes", "kb", "mb", "gb", "tb", "pb"]:
            if unit != "bytes":
                size *= 0.001
            if size < 1000 or unit == "pb":
                return f"{round(size, 2)} {unit}"

    def is_larger(self, path: Self) -> bool:
        """Returns whether this file or folder is larger than
        the one pointed to by 'path'."""
        return self.size() > path.size()

    def is_older(self, path: Self) -> bool:
        """Returns whether this file or folder is older than
        the one pointed to by 'path'."""
        return self.dob < path.dob

    def modified_more_recently(self, path: Self) -> bool:
        """Returns whether this file or folder was modified
        more recently than the one pointed to by 'path'."""
        return self.mod_date > path.mod_date

    # ===============================================navigation===============================================
    def mkcwd(self):
        """Make this path your current working directory."""
        os.chdir(self)

    @property
    def in_PATH(self) -> bool:
        """Return True if this
        path is in sys.path."""
        return str(self) in sys.path

    def add_to_PATH(self, index: int = 0):
        """Insert this path into sys.path
        if it isn't already there.

        :param index: The index of sys.path
        to insert this path at."""
        path = str(self)
        if not self.in_PATH:
            sys.path.insert(index, path)

    def append_to_PATH(self):
        """Append this path to sys.path
        if it isn't already there."""
        path = str(self)
        if not self.in_PATH:
            sys.path.append(path)

    def remove_from_PATH(self):
        """Remove this path from sys.path
        if it's in sys.path."""
        if self.in_PATH:
            sys.path.remove(str(self))

    def moveup(self, name: str) -> Self:
        """Return a new Pathier object that is a parent of this instance.
        'name' is case-sensitive and raises an exception if it isn't in self.parts.
        >>> p = Pathier("C:\some\directory\in\your\system")
        >>> print(p.moveup("directory"))
        >>> "C:\some\directory"
        >>> print(p.moveup("yeet"))
        >>> "Exception: yeet is not a parent of C:\some\directory\in\your\system" """
        if name not in self.parts:
            raise Exception(f"{name} is not a parent of {self}")
        return Pathier(*(self.parts[: self.parts.index(name) + 1]))

    def __sub__(self, levels: int) -> Self:
        """Return a new Pathier object moved up 'levels' number of parents from the current path.
        >>> p = Pathier("C:\some\directory\in\your\system")
        >>> new_p = p - 3
        >>> print(new_p)
        >>> "C:\some\directory" """
        path = self
        for _ in range(levels):
            path = path.parent
        return path

    def move_under(self, name: str) -> Self:
        """Return a new Pathier object such that the stem
        is one level below the folder 'name'.
        'name' is case-sensitive and raises an exception if it isn't in self.parts.
        >>> p = Pathier("a/b/c/d/e/f/g")
        >>> print(p.move_under("c"))
        >>> 'a/b/c/d'"""
        if name not in self.parts:
            raise Exception(f"{name} is not a parent of {self}")
        return self - (len(self.parts) - self.parts.index(name) - 2)

    def separate(self, name: str, keep_name: bool = False) -> Self:
        """Return a new Pathier object that is the
        relative child path after 'name'.
        'name' is case-sensitive and raises an exception if it isn't in self.parts.

        :param keep_name: If True, the returned path will start with 'name'.
        >>> p = Pathier("a/b/c/d/e/f/g")
        >>> print(p.separate("c"))
        >>> 'd/e/f/g'
        >>> print(p.separate("c", True))
        >>> 'c/d/e/f/g'"""
        if name not in self.parts:
            raise Exception(f"{name} is not a parent of {self}")
        if keep_name:
            return Pathier(*self.parts[self.parts.index(name) :])
        return Pathier(*self.parts[self.parts.index(name) + 1 :])

    # ============================================write and read============================================
    def mkdir(self, mode: int = 511, parents: bool = True, exist_ok: bool = True):
        """Create this directory.
        Same as Path().mkdir() except
        'parents' and 'exist_ok' default
        to True instead of False."""
        super().mkdir(mode, parents, exist_ok)

    def touch(self):
        """Create file and parents if necessary."""
        self.parent.mkdir()
        super().touch()

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

    def copy(
        self, new_path: Self | pathlib.Path | str, overwrite: bool = False
    ) -> Self:
        """Copy the path pointed to by this instance
        to the instance pointed to by new_path using shutil.copyfile
        or shutil.copytree. Returns the new path.

        :param new_path: The copy destination.

        :param overwrite: If True, files already existing in new_path
        will be overwritten. If False, only files that don't exist in new_path
        will be copied."""
        new_path = Pathier(new_path)
        if self.is_dir():
            if overwrite or not new_path.exists():
                shutil.copytree(self, new_path, dirs_exist_ok=True)
            else:
                files = self.rglob("*.*")
                for file in files:
                    dst = new_path.with_name(file.name)
                    if not dst.exists():
                        shutil.copyfile(file, dst)
        elif self.is_file():
            if overwrite or not new_path.exists():
                shutil.copyfile(self, new_path)
        return new_path


class PosixPath(Pathier, pathlib.PurePosixPath):
    __slots__ = ()


class WindowsPath(Pathier, pathlib.PureWindowsPath):
    __slots__ = ()
