from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from autopytest.autotest import Autotest

pytestmark = pytest.mark.filterwarnings(
    "ignore:cannot collect test class 'TestFileStrategy'",
)


@pytest.fixture()
def application_path() -> str:
    return "fixtures/application"


@pytest.fixture()
def library_src_path() -> str:
    return "fixtures/library_src"


def test_should_create_list_of_source_for_application(application_path: str) -> None:
    autotest = Autotest(application_path)

    sources = autotest.sources
    assert sources[0].directory == "app"
    assert sources[1].directory == "lib"


def test_should_create_list_of_source_for_library(library_src_path: str) -> None:
    autotest = Autotest(library_src_path)

    sources = autotest.sources
    assert sources[0].directory == "src"


@patch("autopytest.strategy.TestFileStrategy.execute")
def test_match_strategy_with_test_file_strategy(mock_execute: MagicMock) -> None:
    autotest = Autotest("fixtures/application")

    path = Path("fixtures/application/tests/test_module.py").absolute()

    autotest.match_strategy(path)

    mock_execute.assert_called_once()


@patch("autopytest.strategy.SourceFileStrategy.execute")
def test_match_strategy_with_source_file_strategy(mock_execute: MagicMock) -> None:
    autotest = Autotest("fixtures/application")

    path = Path("fixtures/application/app/module.py").absolute()

    autotest.match_strategy(path)

    mock_execute.assert_called_once()
