# Changelog

## v1.1.0 (2023-07-02)

#### New Features

* add `formatted_size` property
#### Docs

* update readme

## v1.0.0 (2023-07-02)

#### Performance improvements

* BREAKING: replace() accepts a list of 2-tuples instead of only an old and new string
#### Refactorings

* BREAKING: change `format_size()` to `format_bytes()`
* BREAKING: change `size` to a property
#### Docs

* update readme

## v0.14.1 (2023-06-21)

#### Performance improvements

* toml files will have their datatypes converted to python types when loaded
#### Others

* specify minimum tomlkit version
## v0.14.0 (2023-06-10)

#### New Features

* add type aliases for `Pathier | pathlib.Path` and `Pathier | pathlib.Path | str`
## v0.13.0 (2023-06-01)

#### Refactorings

* size() returns 0 for non-existent files instead of None

## v0.12.0 (2023-05-26)

#### New Features

* add `keepends` parameter to split function
* add `sep` parameter to join function
* add properties to track last read vs last modified times
#### Others



## v0.11.0 (2023-04-29)

#### New Features

* add join and split methods
* add append method
#### Docs

* update readme


## v0.10.0 (2023-04-29)

#### New Features

* add replace function
* add execute function
#### Docs

* update readme
* improve doc string formatting
#### Others

* build v0.10.0
* update changelog
* remove unused import


## v0.9.0 (2023-04-28)

#### New Features

* add backup function
#### Others

* build v0.9.0
* update changelog


## v0.8.0 (2023-04-15)

#### New Features

* wrap importing typing.Self in try/except to accomodate python 3.10
#### Refactorings

* import Self from typing_extensions
#### Others

* build v0.8.0
* update changelog
* remove uneeded dependency
* set requires-python to >=3.10
* build v0.7.0
* remove uneeded dependency


## v0.7.0 (2023-04-11)

#### New Features

* add remove_from_PATH and make in_PATH a property
* add functions to add path to sys.path
* add 'PathLike' reference for annotating types that can be Pathier, pathlib.Path, or str
#### Others

* build v0.7.0
* update changelog
* update readme


## v0.6.0 (2023-04-02)

#### New Features

* add mkcwd() method
#### Others

* build v0.6.0
* update changelog
* update readme


## v0.5.0 (2023-04-01)

#### New Features

* add separate() method
#### Fixes

* separate() returned tuple instead of new Pathier object
#### Others

* build v0.5.0
* update changelog
* update readme


## v0.4.0 (2023-04-01)

#### New Features

* add move_under() method
#### Others

* build v0.4.0
* update changelog
* update readme


## v0.3.0 (2023-03-31)

#### New Features

* add modified_more_recently()
* add is_older()
* add is_larger() method
* add mod_delta property
* add mod_time property
* add dob property
* add age property
* add format arg to size()
* add format_size() static method
* add size property
#### Fixes

* remove some erroneous text that found its way into some doc strings
#### Refactorings

* remove time module import
* rename mod_time to mod_date
* change size from property to function
#### Others

* build v0.3.0
* update changelog
* add to readme
* remove unused import


## v0.2.0 (2023-03-31)

#### New Features

* add moveup() and __sub__() methods
#### Others

* build v0.2.0
* update changelog
* update readme
* change __sub__ docstring


## v0.1.0 (2023-03-31)

#### New Features

* add touch()
#### Others

* build v0.1.0
* update changelog
* update .gitignore


## v0.0.0 (2023-03-28)

#### New Features

* add copy method to Pathier class.
#### Fixes

* wrong string in __all__.
#### Others

* build v0.0.0
* add to readme.
* add test for copy function.