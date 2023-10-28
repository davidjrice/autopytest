from autopytest.config import Config


def test_should_parse_library_config_with_src_directory() -> None:
    config = Config.parse("tests/fixtures/library_src")
    assert config.source_directories == ["src"]
    assert config.test_directory == "tests"
    assert config.include_source_dir_in_test_path is False


def test_should_parse_library_config_with_package_directory() -> None:
    config = Config.parse("tests/fixtures/library_pkg")
    assert config.source_directories == ["package"]
    assert config.test_directory == "tests"
    assert config.include_source_dir_in_test_path is True


def test_should_parse_application_config() -> None:
    config = Config.parse("tests/fixtures/application")
    assert config.source_directories == ["app", "lib"]
    assert config.test_directory == "tests"
    assert config.include_source_dir_in_test_path is True


def test_should_create_list_of_source() -> None:
    config = Config.parse("tests/fixtures/application")

    sources = config.sources
    assert sources[0].directory == "app"
    assert sources[1].directory == "lib"
