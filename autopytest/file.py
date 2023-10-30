from functools import cached_property
from pathlib import Path

from .source import Source


class File:
    def __init__(self, path: Path, source: Source, test_directory: str) -> None:
        self.path = path
        self.source = source
        self.test_path_components: list[str] = [test_directory]
        self.path_components: list[str] = list(
            self.source.relative_path(self.path).parts,
        )

    @cached_property
    def test_path(self) -> Path:
        if self.source.include_in_test_path(self.path_components[0]):
            self.path_components.pop(0)

        file_name = self.path_components.pop()
        self.test_path_components.extend(self.path_components)
        self.test_path_components.append(f"test_{file_name}")

        test_path = "/".join(self.test_path_components)
        return Path(test_path)
