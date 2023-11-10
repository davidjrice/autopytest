import subprocess
from typing import Final


class Pytest:
    ARGS: Final[list] = [
        "pytest",
        "--no-header",
    ]

    @classmethod
    def run(cls, path: str, args: list[str] | None = None) -> int:
        args = args or []
        return subprocess.call(cls.args(path, args))  # noqa: S603

    @classmethod
    def args(cls, path: str, args: list[str] | None = None) -> list[str]:
        args = args or []
        return [*cls.ARGS + args, path]
