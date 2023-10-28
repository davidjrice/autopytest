import logging as log
import re
import sys
import time
from pathlib import Path

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from .config import Config
from .file import File
from .runners.pytest import Pytest
from .source import Source


class Autotest(FileSystemEventHandler):
    def __init__(self, path: str) -> None:
        log.basicConfig(
            format="[autopytest] %(message)s",
            stream=sys.stdout,
            level=log.INFO,
        )
        self.config = Config.parse(path)
        log.debug(self.config)

        self.sources: list[Source] = []
        for directory in self.config.source_directories:
            source = Source(directory=directory, path=path)
            source.include_directory_in_test_path = (
                self.config.include_source_dir_in_test_path
            )
            self.sources.append(source)
            log.info(f"{source.directory} {source.pattern}")

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

        if path.is_dir():
            return

        if re.search(self.config.ignore_pattern, matcher):
            return

        log.info(f"{event.event_type} {event.src_path}")

        for source in self.sources:
            if re.search(source.pattern, matcher):
                log.info(f"{event.event_type} {event.src_path}")
                source_file = File(
                    path=path,
                    source=source,
                    test_directory=self.config.test_directory,
                )

                if source_file.test_path.exists():
                    if Pytest.run(source_file.test_path) == 0:
                        Pytest.run(".")
                else:
                    log.info(
                        f"{source_file.path} - no matching test found at: {source_file.test_path}",
                    )
                    Pytest.run(".")

        if re.search(self.config.test_pattern, matcher):
            log.info(f"{event.event_type} {matcher}")
            if Pytest.run(matcher) == 0:
                Pytest.run(".")
