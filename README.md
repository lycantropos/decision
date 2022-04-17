decision
========

[![](https://github.com/lycantropos/decision/workflows/CI/badge.svg)](https://github.com/lycantropos/decision/actions/workflows/ci.yml "Github Actions")
[![](https://codecov.io/gh/lycantropos/decision/branch/master/graph/badge.svg)](https://codecov.io/gh/lycantropos/decision "Codecov")
[![](https://img.shields.io/github/license/lycantropos/decision.svg)](https://github.com/lycantropos/decision/blob/master/LICENSE "License")
[![](https://badge.fury.io/py/decision.svg)](https://badge.fury.io/py/decision "PyPI")

In what follows `python` is an alias for `python3.6` or `pypy3.6`
or any later version (`python3.7`, `pypy3.7` and so on).

Installation
------------

Install the latest `pip` & `setuptools` packages versions
```bash
python -m pip install --upgrade pip setuptools
```

### User

Download and install the latest stable version from `PyPI` repository
```bash
python -m pip install --upgrade decision
```

### Developer

Download the latest version from `GitHub` repository
```bash
git clone https://github.com/lycantropos/decision.git
cd decision
```

Install
```bash
python setup.py install
```

Usage
-----
```python
>>> from decision.partition import coin_change
>>> coin_change(10, [2])
(2, 2, 2, 2, 2)
>>> coin_change(10, [2, 3])
(2, 2, 3, 3)
>>> coin_change(10, [2, 3, 4])
(2, 4, 4)
>>> coin_change(10, [2, 3, 4, 5])
(5, 5)

```

Development
-----------

### Bumping version

#### Preparation

Install
[bump2version](https://github.com/c4urself/bump2version#installation).

#### Pre-release

Choose which version number category to bump following [semver
specification](http://semver.org/).

Test bumping version
```bash
bump2version --dry-run --verbose $CATEGORY
```

where `$CATEGORY` is the target version number category name, possible
values are `patch`/`minor`/`major`.

Bump version
```bash
bump2version --verbose $CATEGORY
```

This will set version to `major.minor.patch-alpha`. 

#### Release

Test bumping version
```bash
bump2version --dry-run --verbose release
```

Bump version
```bash
bump2version --verbose release
```

This will set version to `major.minor.patch`.

### Running tests

Install dependencies
```bash
python -m pip install -r requirements-tests.txt
```

Plain
```bash
pytest
```

Inside `Docker` container:
- with `CPython`
  ```bash
  docker-compose --file docker-compose.cpython.yml up
  ```
- with `PyPy`
  ```bash
  docker-compose --file docker-compose.pypy.yml up
  ```

`Bash` script:
- with `CPython`
  ```bash
  ./run-tests.sh
  ```
  or
  ```bash
  ./run-tests.sh cpython
  ```

- with `PyPy`
  ```bash
  ./run-tests.sh pypy
  ```

`PowerShell` script:
- with `CPython`
  ```powershell
  .\run-tests.ps1
  ```
  or
  ```powershell
  .\run-tests.ps1 cpython
  ```
- with `PyPy`
  ```powershell
  .\run-tests.ps1 pypy
  ```
