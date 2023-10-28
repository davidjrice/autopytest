import re
from pathlib import Path


class Source:
    def __init__(self, directory: str, path: str) -> None:
        self._directory = directory
        self._parent = Path(path)
        self.include_directory_in_test_path = True

    @property
    def directory(self) -> str:
        return self._directory

    @property
    def parent(self) -> Path:
        return self._parent

    @property
    def path(self) -> Path:
        return self.parent.joinpath(self._directory)

    @property
    def absolute(self) -> Path:
        return self.path.absolute()

    @property
    def posix(self) -> str:
        return self.absolute.as_posix()

    @property
    def pattern(self) -> str:
        return r"^" + re.escape(self.posix) + r".+\.py$"

    def include_in_test_path(self, path: str) -> bool:
        return not self.include_directory_in_test_path and path == self.directory

    def relative_path(self, path: Path) -> Path:
        return path.relative_to(self.parent.absolute())
