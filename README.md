An implementation of `autotest` for Python inspired by [autotest](https://github.com/grosser/autotest) and [guard](https://github.com/guard/guard).

Autopytest observes file change events and whenever you save a file it runs the appropriate test.

# Install
```
poetry add autopytest
```

# Configuration

```toml
[tool.autopytest]
source_directories = ["app", "lib"]
test_directory = "tests"
```

## Test Naming

Test naming is *currently* important. For example given the above configuration if `app/models/order.py` is edited we will attempt to locate and run `tests/app/models/test_order.py`

# Usage
```
cd <project>
autopytest
```

