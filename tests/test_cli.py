from unittest.mock import MagicMock, patch

from autopytest.cli import main


@patch("sys.argv", return_value=[])
@patch("autopytest.cli.Autotest")
def test_should_start_autotest(mock_autotest: MagicMock, _mock_argv: MagicMock) -> None:
    main()
    mock_autotest.assert_called_with(".")
