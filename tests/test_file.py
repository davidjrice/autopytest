from pathlib import Path

import pytest

from autopytest.config import Config
from autopytest.file import File


@pytest.fixture()
def application_config() -> Config:
    return Config.parse("tests/fixtures/application")


@pytest.fixture()
def library_src_config() -> Config:
    return Config.parse("tests/fixtures/library_src")


def test_should_generate_test_path_for_application(application_config: Config) -> None:
    file = File(
        path=Path("tests/fixtures/application/app/calculator.py").absolute(),
        source=application_config.sources[0],
        config=application_config,
    )
    assert file.test_path == Path("tests/app/test_calculator.py")


def test_should_generate_test_path_for_library(library_src_config: Config) -> None:
    file = File(
        path=Path("tests/fixtures/library_src/src/calculator.py").absolute(),
        source=library_src_config.sources[0],
        config=library_src_config,
    )
    assert file.test_path == Path("tests/test_calculator.py")
