# TODO

* Version pre
  * ~initial version~
* Version 0.0.1
  * ~allow configuration of source and test directories via `pyproject.toml`~
* Version 0.0.2
  * ~improved logging~
    * ~adds logging for when a file is modified~
    * ~adds logging for when a test file cannot be found~
  * ~if there is no matching unit test file, run the entire suite~
* Future
  * allow configuration of matchers in case of using a different directory structure
  * parse pytest results
  * send notifications via 'terminal-notifier'
  * support notifications from within a docker container
  * support linters?
