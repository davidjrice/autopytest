import re
from pathlib import Path

from .config import Config
from .source import Source


class File:
    def __init__(self, path: Path, source: Source, config: Config) -> None:
        self.path = path
        self.config = config
        self.source = source

    @property
    def test_path(self) -> Path:
        test_path_components: list[str] = [self.config.test_directory]
        path_components: list[str] = list(self.source.relative_path(self.path).parts)
        if (
            not self.config.include_source_dir_in_test_path
            and path_components[0] == self.source.directory
        ):
            path_components.pop(0)

        for component in path_components:
            if re.search(r"\.py", component):
                test_path_components.append(f"test_{component}")
            else:
                test_path_components.append(component)

        test_path = "/".join(test_path_components)
        return Path(test_path)
