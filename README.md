# `autopytest`

[![PyPI version][pypi-badge]][pypi-link]
[![Python versions][python-versions-badge]][pypi-link]
[![Build Status][build-badge]][build-link]
[![Maintainability][maintainability-badge]][maintainability-link]
[![Test Coverage][coverage-badge]][coverage-link]

An implementation of `autotest` for Python inspired by [autotest][] and [guard][].

[autopytest](pypi-link) observes file change events and whenever you save a file it runs the appropriate tests with `pytest`.

## Features

`autopytest` observes file `modified` events and will perform the following:

* source files
  * will find and run the associated individual test file
  * upon success, will run the entire suite
  * if we can't find a matching test, run the entire suite
* test files
  * will run that test file
  * upon success, will run the entire suite

## Install

```shell
# pip
pip install autopytest

# poetry
poetry add autopytest
```

## Configuration

In your `pyproject.toml` add the following.

```toml
[tool.autopytest]
source_directories = ["app"]
test_directory = "tests"
```

## Usage

```shell
cd {project}
autopytest

autopytest {path}
```

## Project Structure

* Test naming is *currently* important.
* Multiple nested directory structures are supported as long as the convention is followed.

### Applications

#### `pyproject.toml` for applications

```toml
[tool.autopytest]
source_directories = ["app", "lib"]
test_directory = "tests"
```

Given the above configuration. You should use a directory structure like the following. e.g. If `app/package/module.py` is edited we will attempt to locate and run `tests/app/package/test_module.py`

```markdown
📁 app
    📄 __init__.py
    📁 package
        📄 __init__.py
        📄 module.py
📁 lib
📁 tests
    📄 __init__.py
    📁 app
        📁 package
            📄 test_module.py
    📁 lib
```

### Libraries

#### `pyproject.toml` for libraries

```toml
[tool.autopytest]
include_source_dir_in_test_path = false
source_directories = ["src"]
test_directory = "tests"
```

If you are developing library and want your folder structure like the following. e.g. If `src/package/module.py` is edited we will attempt to locate and run `tests/package/test_module.py`

```markdown
📁 src
    📁 package
        📄 __init__.py
        📄 module.py
📁 tests
    📁 package
        📄 test_module.py
```

[autotest]: https://github.com/grosser/autotest
[guard]: https://github.com/guard/guard
[maintainability-badge]: https://api.codeclimate.com/v1/badges/f0ec7e4071d41519de65/maintainability
[maintainability-link]: https://codeclimate.com/github/davidjrice/autopytest/maintainability
[coverage-badge]: https://api.codeclimate.com/v1/badges/f0ec7e4071d41519de65/test_coverage
[coverage-link]: https://codeclimate.com/github/davidjrice/autopytest/test_coverage
[build-badge]: https://github.com/davidjrice/autopytest/actions/workflows/tests.yml/badge.svg
[build-link]: https://github.com/davidjrice/autopytest/actions/workflows/tests.yml
[pypi-badge]: https://badge.fury.io/py/autopytest.svg
[pypi-link]: https://pypi.org/project/autopytest/
[python-versions-badge]: https://img.shields.io/pypi/pyversions/autopytest.svg
