An implementation of `autotest` for Python inspired by [autotest](https://github.com/grosser/autotest) and [guard](https://github.com/guard/guard).

Autotest observes file change events and whenever you save a file it runs the appropriate test.

# Install
```
poetry add autopytest
```

# Usage
```
cd <project>
autopytest
```

# Configuration

Autotest currently assumes your directory structure is the following:

* `app` - application code
* `lib` - library code
* `tests` - tests

For example `app/models/order.py` will attempt to locate `tests/app/models/test_order.py`
