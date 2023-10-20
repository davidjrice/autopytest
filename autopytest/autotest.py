import logging as log
import re
import sys
import time
from pathlib import Path

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from .config import parse_pyproject_toml
from .pytest_runner import PytestRunner
from .source import Source


class Autotest(FileSystemEventHandler):
    def __init__(self, path: str) -> None:
        log.basicConfig(
            format="[autopytest] %(message)s",
            stream=sys.stdout,
            level=log.INFO,
        )
        self.observer = Observer()
        self.observer.schedule(self, path, recursive=True)
        self.config = parse_pyproject_toml(f"{path}/pyproject.toml")

        self.include_source_dir_in_test_path = self.config[
            "include_source_dir_in_test_path"
        ]
        self.source_directories = self.config["source_directories"]
        self.test_directory = self.config["test_directory"]

        self.sources = []
        for directory in self.source_directories:
            source = Source(directory=directory, path=path)
            self.sources.append(source)
            log.info(f"{source.directory} {source.pattern}")
        self.test_path = Path(path).absolute().joinpath(self.test_directory)
        self.test_pattern = re.escape(self.test_path.as_posix()) + r".+\.py$"

    def start(self) -> None:
        self.observer.start()

        log.info("started ✅")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            log.info("👋")
            sys.exit(0)
        finally:
            self.observer.stop()
            self.observer.join()

    def on_modified(self, event: FileSystemEvent) -> None:
        path = Path(event.src_path).absolute()
        matcher = path.as_posix()
        for source in self.sources:
            if re.search(source.pattern, matcher):
                log.info(f"{event.event_type} {event.src_path}")

                log.info(f"{path}")
                test_path_components = ["tests"]

                for component in path.relative_to(source.path.parent).parts:
                    if (
                        not self.include_source_dir_in_test_path
                        and component == source.directory
                    ):
                        continue

                    if re.search(r".py", component):
                        test_path_components.append(f"test_{component}")
                    else:
                        test_path_components.append(component)

                test_path = "/".join(test_path_components)
                if Path(test_path).exists():
                    if PytestRunner.run(test_path) == 0:
                        PytestRunner.run(".")
                else:
                    log.info(f"{path} - no matching test found at: {test_path}")
                    PytestRunner.run(".")

        if re.search(self.test_pattern, matcher):
            log.info(f"{event.event_type} {matcher}")
            if PytestRunner.run(matcher) == 0:
                PytestRunner.run(".")
