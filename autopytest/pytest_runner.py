import subprocess
from pathlib import Path
from typing import Final


class PytestRunner:
    ARGS: Final[list] = [
        "pytest",
    ]

    @classmethod
    def run(cls, path: str | Path) -> int:
        if type(path) is Path:
            path = path.as_posix()
        return subprocess.call([*cls.ARGS, path])  # noqa: S603
