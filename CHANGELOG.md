# Changelog

## 0.5.0 (2023-04-01)

#### New Features

* add separate() method
#### Fixes

* separate() returned tuple instead of new Pathier object
#### Others

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