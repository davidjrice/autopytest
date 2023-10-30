from pathlib import Path

import pytest

from autopytest.autotest import Autotest
from autopytest.file import File


@pytest.fixture()
def application_path() -> str:
    return "fixtures/application"


@pytest.fixture()
def library_src_path() -> str:
    return "fixtures/library_src"


def test_should_generate_test_path_for_application(application_path: str) -> None:
    autotest = Autotest(application_path)
    source_file = File(
        path=Path("fixtures/application/app/calculator.py").absolute(),
        source=autotest.sources[0],
        test_directory=autotest.config.test_directory,
    )
    assert source_file.test_path == Path("tests/app/test_calculator.py")


def test_should_generate_test_path_for_library(library_src_path: str) -> None:
    autotest = Autotest(library_src_path)
    source_file = File(
        path=Path("fixtures/library_src/src/calculator.py").absolute(),
        source=autotest.sources[0],
        test_directory=autotest.config.test_directory,
    )
    assert source_file.test_path == Path("tests/test_calculator.py")
