import re
from pathlib import Path


class Source:
    def __init__(self, directory: str, path: str) -> None:
        self._directory = directory
        self._parent = Path(path)

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
