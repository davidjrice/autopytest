An implementation of `autotest` for Python inspired by [autotest](https://github.com/grosser/autotest) and [guard](https://github.com/guard/guard).

[autopytest](https://pypi.org/project/autopytest/) observes file change events and whenever you save a file it runs the appropriate test and upon success runs your entire test suite.

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
source_directories = ["app", "lib"]
test_directory = "tests"
```

## Test Naming

Test naming is *currently* important. For example given the above configuration if `app/models/order.py` is edited we will attempt to locate and run `tests/app/models/test_order.py`

# Usage

```shell
cd {project}
autopytest

autopytest {path}
```

