from pathlib import Path
from unittest.mock import MagicMock, call, patch

from autopytest.autotest import Autotest
from autopytest.file import File
from autopytest.strategy import SourceFileStrategy


@patch("autopytest.strategy.Pytest.run")
def test_execute(mock_run: MagicMock) -> None:
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
