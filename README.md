[![Maintainability](https://api.codeclimate.com/v1/badges/f0ec7e4071d41519de65/maintainability)](https://codeclimate.com/github/davidjrice/autopytest/maintainability)

[![Test Coverage](https://api.codeclimate.com/v1/badges/f0ec7e4071d41519de65/test_coverage)](https://codeclimate.com/github/davidjrice/autopytest/test_coverage)

An implementation of `autotest` for Python inspired by [autotest](https://github.com/grosser/autotest) and [guard](https://github.com/guard/guard).

[autopytest](https://pypi.org/project/autopytest/) observes file change events and whenever you save a file it runs the appropriate tests with `pytest`.

# Features
`autopytest` observes file `modified` events and will perform the following:

* source files
  * will find and run the associated individual test file
  * upon success, will run the entire suite
  * if we can't find a matching test, run the entire suite
* test files
  * will run that test file
  * upon success, will run the entire suite
* pytest configuration
  * supports configuration of different args to pass to pytest on a per unit or per suite basis

# Install

```shell
# pip
pip install autopytest

# poetry
poetry add --group dev autopytest
```

# Configuration

* `source_directories`: the directories of your source code
* `test_directory`: the directory of your test code
* `include_source_dir_in_test_path`: whether or not to include the source directory when inferring the test path
* `pytest_unit_args`: the args to pass to pytest when running a `unit` test
* `pytest_suite_args`: the args to pass to pytest when running the entire test `suite`

In your `pyproject.toml` add the following minimal configuration:

```toml
[tool.autopytest]
source_directories = ["app"]
test_directory = "tests"
```

## `pytest` args

We (currently) automatically add the option `--no-header` to the `pytest` args to ensure that the output is consistent and easy to read/parse.

* NOTE: when using with `pytest-cov` we recommend not adding `--cov` options to your default `pytest` args in `pyproject.toml` to ensure debugger support

```toml
[tool.autopytest]
source_directories = ["app"]
test_directory = "tests"
pytest_unit_args = ["--failed-first", "--newest-first"]
pytest_suite_args = ["--cov", "--no-cov-on-fail", "--failed-first", "--newest-first"]
```

# Usage

```shell
cd {project}
autopytest

autopytest {path}
```

# Project Structure

* Test naming is *currently* important.
* Multiple nested directory structures are supported as long as the convention is followed.

## Applications

### `pyproject.toml`
```toml
[tool.autopytest]
source_directories = ["app", "lib"]
test_directory = "tests"
```

Given the above configuration. You should use a directory structure like the following. e.g. If `app/package/module.py` is edited we will attempt to locate and run `tests/app/package/test_module.py`

```
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

## Libraries

### `pyproject.toml`
```toml
[tool.autopytest]
include_source_dir_in_test_path = false
source_directories = ["src"]
test_directory = "tests"
```

If you are developing library and want your folder structure like the following. e.g. If `src/package/module.py` is edited we will attempt to locate and run `tests/package/test_module.py`

```
📁 src
    📁 package
        📄 __init__.py
        📄 module.py
📁 tests
    📁 package
        📄 test_module.py
```
