import logging as log
from pathlib import Path

from .file import File
from .runners.pytest import Pytest


class Strategy:
    def __init__(self, path_or_file: str | Path | File) -> None:
        if isinstance(path_or_file, str):
            self._path = Path(path_or_file)
        elif isinstance(path_or_file, File):
            self._file = path_or_file
        else:
            self._path = path_or_file

    def execute(self) -> bool:
        return Pytest.run(".") == 0

    @property
    def test_path(self) -> str:
        if self._file:
            return self._file.test_path.as_posix()
        return self._path.as_posix()

    @property
    def test_path_exists(self) -> bool:
        return self._path.exists()


class SourceFileStrategy(Strategy):
    def execute(self) -> bool:
        if not self.test_path_exists:
            log.info(
                f"{self._file.path} - no matching test found at: {self.test_path}",
            )

        return Pytest.run(self.test_path) == 0 and super().execute()


class TestFileStrategy(Strategy):
    def execute(self) -> bool:
        return Pytest.run(self.test_path) == 0 and super().execute()
