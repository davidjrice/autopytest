from unittest.mock import MagicMock, patch

from autopytest.runners.pytest import Pytest


def test_pytest() -> None:
    assert Pytest.args("tests/test_calculator.py") == [
        "pytest",
        "--no-cov",
        "--no-header",
        "tests/test_calculator.py",
    ]


@patch("autopytest.runners.pytest.subprocess")
def test_pytest_run(mock_subprocess: MagicMock) -> None:
    Pytest.run(".")
    mock_subprocess.call.assert_called_with(["pytest", "--no-cov", "--no-header", "."])


@patch("autopytest.runners.pytest.subprocess")
def test_pytest_run_with_path(mock_subprocess: MagicMock) -> None:
    path = "tests/test_calculator.py"
    Pytest.run(path)
    mock_subprocess.call.assert_called_with(["pytest", "--no-cov", "--no-header", path])
