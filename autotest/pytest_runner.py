import subprocess
from typing import Final

class PytestRunner:
    ARGS: Final[list] = [
        "/usr/bin/env",
        "pytest",
        "-vvv",
        "--cov=app/",
        "--cov=lib/",
        "--capture=no",
        "-m",
        "not integration",
    ]

    @classmethod
    def run(cls, path: str) -> int:
        return subprocess.call([*cls.ARGS, path])  # noqa: S603