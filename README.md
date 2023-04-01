# pathier

Extends the standard library pathlib.Path class.

## Installation

Install with:

<pre>
pip install pathier
</pre>



## Usage

Functions the same as pathlib.Path, but with added functions and some altered default arguments.<br>

#### Navigation

New paths can be obtained by:<br>
* naming the parent with moveup()
* subtracting a number of levels from the current path
* naming the parent of the path you actually want with move_under()
<pre>
>>> from pathier import Pathier
>>> path = Pathier("C:/some/directory/to/some/file/on/the/system")
>>> path.moveup("directory")
WindowsPath('C:/some/directory')
>>> path - 3
WindowsPath('C:/some/directory/to/some/file')
>>> path.move_under("directory")
WindowsPath('C:/some/directory/to')
</pre>

#### Manipulation

Can dump and load toml and json files without needed to explicityly import and call functions from the respective libraries:
<pre>
from pathier import Pathier
path = Pathier("some_file.toml")
content = path.loads()
path.with_suffix(".json").dumps(content, indent=2)
</pre>

`Pathier().mkdir()` creates parent directories and doesn't throw an error if the path already exists by default.<br>

`Pathier().write_text()` and `Pathier().write_bytes()` will create parent directories by default if they won't exist.<br>

`Pathier().write_text()` will also try to cast the data to be written to a string if a TypeError is thrown.<br>

`Pathier().delete()` will delete a file or directory, event if that directory isn't empty.<br>

`Pathier().copy()` will copy a file or a directory tree to a new destination and return a Pathier object for the new path<br>
By default, files in the destination will not be overwritten.

#### Stats and Comparisons
<pre>
>>> from pathier import Pathier
>>> p = Pathier.cwd() / "pathier.py"
>>> i = p.parent / "__init__.py"
>>> p.dob
datetime.datetime(2023, 3, 31, 18, 43, 12, 360000)
>>> p.age
8846.024934
>>> p.mod_date
datetime.datetime(2023, 3, 31, 21, 7, 30)
>>> p.mod_delta
207.488857
>>> p.size()
10744
>>> p.size(True)
'10.74 kb'
>>> p.is_larger(i)
True
>>> p.is_older(i)
False
>>> p.modified_more_recently(i)
True
</pre>


