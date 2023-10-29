from pathlib import Path
from unittest.mock import MagicMock, call, patch

from autopytest.autotest import Autotest
from autopytest.file import File
from autopytest.strategy import SourceFileStrategy, TestFileStrategy


@patch("autopytest.strategy.Pytest.run")
def test_execute_source_file_strategy(mock_run: MagicMock) -> None:
    mock_run.return_value = 0
    autotest = Autotest("fixtures/application")
    source_file = File(
        path=Path("fixtures/application/app/module.py").absolute(),
        source=autotest.sources[0],
        test_directory=autotest.config.test_directory,
    )

    strategy = SourceFileStrategy(source_file)
    result = strategy.execute()

    assert result
    mock_run.assert_has_calls(
        [
            call("tests/app/test_module.py"),
            call("."),
        ],
    )


@patch("autopytest.strategy.Pytest.run")
def test_execute_test_file_strategy(mock_run: MagicMock) -> None:
    mock_run.return_value = 0
    autotest = Autotest("fixtures/application")

    path = Path("fixtures/application/tests/test_module.py").absolute()
    path = path.relative_to(autotest.config.path.absolute())

    strategy = TestFileStrategy(path)
    result = strategy.execute()

    assert result
    mock_run.assert_has_calls(
        [
            call("tests/test_module.py"),
            call("."),
        ],
    )
