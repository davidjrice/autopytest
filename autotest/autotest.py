import logging as log
import re
import sys
import time
from pathlib import Path
from typing import Final

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
from .pytest_runner import PytestRunner

class Autotest(FileSystemEventHandler):
    SOURCE_PATTERNS: Final[list] = [
        r"app.+\.py$",
        r"lib.+\.py$",
    ]
    TEST_PATTERN: Final[str] = r"tests.+\.py$"


    def __init__(self, path:str):
        log.basicConfig(level=log.INFO)
        self.observer = Observer()
        self.observer.schedule(self.on_modified, path, recursive=True)

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
        for pattern in self.SOURCE_PATTERNS:
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
            re.search(self.TEST_PATTERN, event.src_path)
            and PytestRunner.run(event.src_path) == 0
        ):
            PytestRunner.run(".")




