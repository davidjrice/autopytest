import subprocess
from typing import Final, List

class PytestRunner:
    ARGS: Final[List[str]] = [
        "/usr/bin/env",
        "pytest",
    ]

    @classmethod
    def run(cls, path: str, extra_args: List[str] = []) -> int:
        return subprocess.call([*cls.ARGS, *extra_args, path])  # noqa: S603