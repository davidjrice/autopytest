import subprocess
from pathlib import Path
from typing import Final


class Pytest:
    ARGS: Final[list] = [
        "pytest",
        "--no-cov",
        "--no-header",
    ]

    @classmethod
    def run(cls, path: str | Path) -> int:
        if not isinstance(path, str):
            path = path.as_posix()
        return subprocess.call(cls.args(path))  # noqa: S603

    @classmethod
    def args(cls, path: str) -> list[str]:
        return [*cls.ARGS, path]
