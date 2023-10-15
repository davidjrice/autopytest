from .autotest import Autotest
import sys
from .commands import init_command 

def cli() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "init":
        init_command.init()
        sys.exit(0)
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    autotest = Autotest(path)
    autotest.start()

def main() -> None:
    cli()