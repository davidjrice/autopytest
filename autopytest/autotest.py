import logging as log
import re
import sys
import time
from pathlib import Path

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from .config import Config
from .pytest_runner import PytestRunner


class Autotest(FileSystemEventHandler):
    def __init__(self, path: str) -> None:
        log.basicConfig(
            format="[autopytest] %(message)s",
            stream=sys.stdout,
            level=log.INFO,
        )
        self.config = Config.parse(path)
        log.debug(self.config)
        self.observer = Observer()
        self.observer.schedule(self, path, recursive=True)

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
        path: Path = Path(event.src_path).absolute()
        matcher: str = path.as_posix()

        if re.search(self.config.ignore_pattern, matcher):
            return

        log.info(f"{event.event_type} {event.src_path}")

        for source in self.config.sources:
            if re.search(source.pattern, matcher):
                log.info(f"{event.event_type} {event.src_path}")

                test_path_components: list[str] = [self.config.test_directory]
                path_components: list[str] = list(
                    path.relative_to(source.path.parent.absolute()).parts,
                )
                if (
                    not self.config.include_source_dir_in_test_path
                    and path_components[0] == source.directory
                ):
                    path_components.pop(0)

                for component in path_components:
                    if re.search(r"\.py", component):
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

        if re.search(self.config.test_pattern, matcher):
            log.info(f"{event.event_type} {matcher}")
            if PytestRunner.run(matcher) == 0:
                PytestRunner.run(".")
