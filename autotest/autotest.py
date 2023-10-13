import logging as log
import re
import sys
import time
from pathlib import Path

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
from .config import parse_pyproject_toml
from .pytest_runner import PytestRunner


class Autotest(FileSystemEventHandler):

    def __init__(self, path:str):
        log.basicConfig(format="%(message)s", stream=sys.stdout, level=log.INFO)
        self.observer = Observer()
        self.observer.schedule(self, path, recursive=True)
        self.config = parse_pyproject_toml(f"{path}/pyproject.toml")
        self.source_directories = self.config["source_directories"]
        self.test_directory = self.config["test_directory"]

        self.source_patterns = []
        for directory in self.source_directories:
            pattern = re.escape(directory) + r".+\.py$"
            self.source_patterns.append(pattern)

        self.test_pattern = re.escape(self.test_directory) + r".+\.py$"


    def start(self) -> None:
        self.observer.start()

        log.info("Autotest started ✅")
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
        for pattern in self.source_patterns:
            if re.search(pattern, event.src_path):
                path = Path(event.src_path)
                test_path_components = ["tests"]

                for component in path.parts:
                    if re.search(r".py", component):
                        test_path_components.append(f"test_{component}")
                    else:
                        test_path_components.append(component)
                test_path = "/".join(test_path_components)
                if Path(test_path).exists() and PytestRunner.run(test_path) == 0:
                    PytestRunner.run(".")

        if (
            re.search(self.test_pattern, event.src_path)
            and PytestRunner.run(event.src_path) == 0
        ):
            PytestRunner.run(".")




