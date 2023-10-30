from autopytest.config import Config


def test_should_parse_library_config_with_src_directory() -> None:
    config = Config.parse("fixtures/library_src")
    assert config.source_directories == ["src"]
    assert config.test_directory == "tests"
    assert config.include_source_dir_in_test_path is False


def test_should_parse_library_config_with_package_directory() -> None:
    config = Config.parse("fixtures/library_pkg")
    assert config.source_directories == ["package"]
    assert config.test_directory == "tests"
    assert config.include_source_dir_in_test_path is True


def test_should_parse_application_config() -> None:
    config = Config.parse("fixtures/application")
    assert config.source_directories == ["app", "lib"]
    assert config.test_directory == "tests"
    assert config.include_source_dir_in_test_path is True


def test_ignore_pattern() -> None:
    config = Config(
        _path=".",
        ignored_patterns=["*.txt", "*.log"],
        source_directories=["src"],
        test_directory="tests",
    )
    assert config.ignore_pattern == "*.txt|*.log"
