* Version pre
  * ~initial version~
* Version 0.0.1
  * ~allow configuration of source and test directories via `pyproject.toml`~
* Version 0.0.2
  * ~improved logging~
    * ~adds logging for when a file is modified~
    * ~adds logging for when a test file cannot be found~
  * ~if there is no matching unit test file, run the entire suite~
* ~allow configuration of matchers in case of using a different directory structure~
* ~allow configuration of pytest args~
* Future
  * remember if the last suite run failed or not and add `--last-failed` if so
  * remember if the last unit run failed or not and add `--last-failed` if so (more difficult as we need to keep track of the unit
  test and the result)
  * ensure debugger support
  * automatic disabling of code coverage (only if it's enabled) when attempting to run in debug mode?
  * parse pytest results
  * send notifications via 'terminal-notifier'
  * support notifications from within a docker container
  * support linters?
