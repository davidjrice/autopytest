import re
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

    @property
    def test_path(self) -> Path:
        if self.source.include_in_test_path(self.path_components[0]):
            self.path_components.pop(0)

        for component in self.path_components:
            if re.search(r"\.py", component):
                self.test_path_components.append(f"test_{component}")
            else:
                self.test_path_components.append(component)

        test_path = "/".join(self.test_path_components)
        return Path(test_path)
