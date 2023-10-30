import logging as log
from pathlib import Path

from .file import File
from .runners.pytest import Pytest


class NoPathOrFileProvidedError(ValueError):
    def __init__(self) -> None:
        super().__init__("No path or file provided")


class Strategy:
    _path: Path | None = None
    _file: File | None = None

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
        if self._path:
            return self._path.as_posix()
        raise NoPathOrFileProvidedError

    @property
    def file_path(self) -> str:
        if self._file:
            return self._file.path.as_posix()
        if self._path:
            return self._path.as_posix()
        raise NoPathOrFileProvidedError

    @property
    def test_path_exists(self) -> bool:
        if self._file:
            return self._file.test_path.exists()
        if self._path:
            return self._path.exists()

        raise NoPathOrFileProvidedError


class SourceFileStrategy(Strategy):
    def execute(self) -> bool:
        if not self.test_path_exists:
            log.info(
                f"{self.file_path} - no matching test found at: {self.test_path}",
            )

        return Pytest.run(self.test_path) == 0 and super().execute()


class TestFileStrategy(Strategy):
    def execute(self) -> bool:
        return Pytest.run(self.test_path) == 0 and super().execute()
