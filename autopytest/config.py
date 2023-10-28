import platform
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from packaging import version

if version.parse(platform.python_version()) < version.parse("3.11"):
    import toml
    from typing_extensions import Self
else:
    from typing import Self

    import tomllib

DEFAULTS = {
    "include_source_dir_in_test_path": True,
    "ignored_patterns": [
        r"__pycache__",
        r"\.cache",
        r"\.coverage",
        r"\.git",
        r"\.mypy_cache",
        r"\.pytest_cache",
        r"\.tox",
    ],
}


@dataclass
class Config:
    _path: str
    ignored_patterns: list[str]
    source_directories: list[str]
    test_directory: str
    include_source_dir_in_test_path: bool = True

    @classmethod
    def parse(cls, path: str) -> Self:
        absolute_path: Path = Path(path).absolute()
        toml: dict = parse_pyproject_toml(f"{absolute_path}/pyproject.toml")
        return cls(_path=path, **toml)

    @property
    def path(self) -> Path:
        return Path(self._path)

    @property
    def test_path(self) -> Path:
        return self.path.absolute().joinpath(self.test_directory)

    @property
    def test_pattern(self) -> str:
        return re.escape(self.test_path.as_posix()) + r".+\.py$"

    @property
    def ignore_pattern(self) -> str:
        return "|".join(self.ignored_patterns)


def parse_pyproject_toml(path: str) -> dict[str, Any]:
    pyproject_toml: dict = {}
    with Path(path).open("rb") as f:
        try:
            pyproject_toml = tomllib.load(f)
        except NameError:
            pyproject_toml = toml.loads(f.read().decode("UTF-8"))

    config: dict[str, Any] = pyproject_toml.get("tool", {}).get("autopytest", {})

    return {**DEFAULTS, **config}  # noqa: RUF100 FURB173
