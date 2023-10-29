import subprocess
from typing import Final


class Pytest:
    ARGS: Final[list] = [
        "pytest",
        "--no-cov",
        "--no-header",
    ]

    @classmethod
    def run(cls, path: str) -> int:
        return subprocess.call(cls.args(path))  # noqa: S603

    @classmethod
    def args(cls, path: str) -> list[str]:
        return [*cls.ARGS, path]
