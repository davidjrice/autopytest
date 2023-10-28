import logging as log
import re
import sys
import time
from pathlib import Path

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from .config import Config
from .file import File
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

                source_file = File(path=path, source=source, config=self.config)

                if source_file.test_path.exists():
                    if PytestRunner.run(source_file.test_path) == 0:
                        PytestRunner.run(".")
                else:
                    log.info(
                        f"{source_file} - no matching test found at: {source_file.test_path}",
                    )
                    PytestRunner.run(".")

        if re.search(self.config.test_pattern, matcher):
            log.info(f"{event.event_type} {matcher}")
            if PytestRunner.run(matcher) == 0:
                PytestRunner.run(".")
