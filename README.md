decision
========

[![](https://travis-ci.com/lycantropos/decision.svg?branch=master)](https://travis-ci.com/lycantropos/decision "Travis CI")
[![](https://dev.azure.com/lycantropos/decision/_apis/build/status/lycantropos.decision?branchName=master)](https://dev.azure.com/lycantropos/decision/_build/latest?definitionId=27&branchName=master "Azure Pipelines")
[![](https://codecov.io/gh/lycantropos/decision/branch/master/graph/badge.svg)](https://codecov.io/gh/lycantropos/decision "Codecov")
[![](https://img.shields.io/github/license/lycantropos/decision.svg)](https://github.com/lycantropos/decision/blob/master/LICENSE "License")
[![](https://badge.fury.io/py/decision.svg)](https://badge.fury.io/py/decision "PyPI")

In what follows
- `python` is an alias for `python3.5` or any later
version (`python3.6` and so on),
- `pypy` is an alias for `pypy3.5` or any later
version (`pypy3.6` and so on).

Installation
------------

Install the latest `pip` & `setuptools` packages versions:
- with `CPython`
  ```bash
  python -m pip install --upgrade pip setuptools
  ```
- with `PyPy`
  ```bash
  pypy -m pip install --upgrade pip setuptools
  ```

### User

Download and install the latest stable version from `PyPI` repository:
- with `CPython`
  ```bash
  python -m pip install --upgrade decision
  ```
- with `PyPy`
  ```bash
  pypy -m pip install --upgrade decision
  ```

### Developer

Download the latest version from `GitHub` repository
```bash
git clone https://github.com/lycantropos/decision.git
cd decision
```

Install dependencies:
- with `CPython`
  ```bash
  python -m pip install --force-reinstall -r requirements.txt
  ```
- with `PyPy`
  ```bash
  pypy -m pip install --force-reinstall -r requirements.txt
  ```

Install:
- with `CPython`
  ```bash
  python setup.py install
  ```
- with `PyPy`
  ```bash
  pypy setup.py install
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

Install dependencies:
- with `CPython`
  ```bash
  python -m pip install --force-reinstall -r requirements-tests.txt
  ```
- with `PyPy`
  ```bash
  pypy -m pip install --force-reinstall -r requirements-tests.txt
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

`Bash` script (e.g. can be used in `Git` hooks):
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

`PowerShell` script (e.g. can be used in `Git` hooks):
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
