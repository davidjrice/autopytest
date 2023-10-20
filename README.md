An implementation of `autotest` for Python inspired by [autotest](https://github.com/grosser/autotest) and [guard](https://github.com/guard/guard).

[autopytest](https://pypi.org/project/autopytest/) observes file change events and whenever you save a file it runs the appropriate test, upon success it runs your entire test suite and if we can't find a matching test file for a given source, we also run the entire suite.

# Install

```shell
# pip
pip install autopytest

# poetry
poetry add autopytest
```

# Configuration

In your `pyproject.toml` add the following.

```python
[tool.autopytest]
source_directories = ["app"]
test_directory = "tests"
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
```python
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
```python
[tool.autopytest]
include_source_dir_in_test_path = False
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
