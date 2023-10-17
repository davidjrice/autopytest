import subprocess
from typing import Final

class PytestRunner:
    ARGS: Final[list] = [
        "pytest",
    ]

    @classmethod
    def run(cls, path: str) -> int:
        return subprocess.call([*cls.ARGS, path])  # noqa: S603