# pathier

Extends the standard library pathlib.Path class.

## Installation

Install with:

<pre>
pip install pathier
</pre>



## Usage

Functions the same as pathlib.Path, but with added functions and some altered default arguments.<br>
Can dump and load toml and json files:
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
