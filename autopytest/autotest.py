import logging
import re
import sys
import time
from pathlib import Path

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer
from watchdog.observers.api import BaseObserver

from .config import Config
from .file import File
from .source import Source
from .strategy import SourceFileStrategy, TestFileStrategy

logging.basicConfig(
    format="[autopytest] %(message)s",
    stream=sys.stdout,
    level=logging.INFO,
)


class Autotest(FileSystemEventHandler):
    _log: logging.Logger = logging.getLogger("autopytest")
    _observer: BaseObserver

    def __init__(self, path: str) -> None:
        self.config = Config.parse(path)
        self.log.debug(self.config)

        self.sources: list[Source] = []
        for directory in self.config.source_directories:
            source = Source(directory=directory, path=path)
            source.include_directory_in_test_path = (
                self.config.include_source_dir_in_test_path
            )
            self.sources.append(source)
            self.log.info(f"{source.directory} {source.pattern}")

        self._observer = Observer()
        self._observer.schedule(self, path, recursive=True)

    def start(self) -> None:
        self.observer.start()

        self.log.info("started")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.log.info("stopping")
            sys.exit(0)
        finally:
            self.observer.stop()
            self.observer.join()

    def on_modified(self, event: FileSystemEvent) -> None:
        path: Path = Path(event.src_path).absolute()
        if path.is_dir() or re.search(self.config.ignore_pattern, path.as_posix()):
            return

        self.log.info(f"{event.event_type} {event.src_path}")
        self.match_strategy(path)

    def match_strategy(self, path: Path) -> None:
        strategy: SourceFileStrategy | TestFileStrategy
        matcher: str = path.as_posix()

        if re.search(self.config.test_pattern, matcher):
            test_path = path.relative_to(self.config.path.absolute())
            strategy = TestFileStrategy(test_path)
            strategy.execute()
            return

        for source in self.sources:
            if re.search(source.pattern, matcher):
                source_file = File(
                    path=path,
                    source=source,
                    test_directory=self.config.test_directory,
                )

                strategy = SourceFileStrategy(source_file)
                strategy.execute()
                return

    @property
    def log(self) -> logging.Logger:
        return self._log

    @property
    def observer(self) -> BaseObserver:
        return self._observer
