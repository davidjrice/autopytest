import logging as log
import re
import sys
import time
from pathlib import Path

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
from .config import parse_pyproject_toml
from .pytest_runner import PytestRunner

class Source:

    def __init__(self, directory) -> None:
        self.directory = directory

    @property
    def pattern(self) -> str:
        return r"^\./" + re.escape(self.directory) + r".+\.py$"


class Autotest(FileSystemEventHandler):

    def __init__(self, path:str):
        log.basicConfig(format="[autopytest] %(message)s", stream=sys.stdout, level=log.INFO)
        self.observer = Observer()
        self.observer.schedule(self, path, recursive=True)
        self.config = parse_pyproject_toml(f"{path}/pyproject.toml")

        self.include_source_dir_in_test_path = self.config["include_source_dir_in_test_path"]
        self.source_directories = self.config["source_directories"]
        self.test_directory = self.config["test_directory"]

        self.sources = []
        for directory in self.source_directories:
            self.sources.append(Source(directory=directory))
        self.test_pattern = re.escape(self.test_directory) + r".+\.py$"


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
        for source in self.sources:
            if re.search(source.pattern, event.src_path):
                log.info(f"{event.event_type} {event.src_path}")
                path = Path(event.src_path)
                test_path_components = ["tests"]

                for component in path.parts:
                    if not self.include_source_directories_in_test_path and component == source.directory:
                        continue
                    elif re.search(r".py", component):
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

        if re.search(self.test_pattern, event.src_path):
            log.info(f"{event.event_type} {event.src_path}")
            if PytestRunner.run(event.src_path) == 0:
                PytestRunner.run(".")




