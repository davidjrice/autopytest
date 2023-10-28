import pytest

from autopytest.autotest import Autotest


@pytest.fixture()
def application_path() -> str:
    return "tests/fixtures/application"


@pytest.fixture()
def library_src_path() -> str:
    return "tests/fixtures/library_src"


def test_should_create_list_of_source_for_application(application_path: str) -> None:
    autotest = Autotest(application_path)

    sources = autotest.sources
    assert sources[0].directory == "app"
    assert sources[1].directory == "lib"


def test_should_create_list_of_source_for_library(library_src_path: str) -> None:
    autotest = Autotest(library_src_path)

    sources = autotest.sources
    assert sources[0].directory == "src"
