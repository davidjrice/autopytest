import platform
from pathlib import Path
from unittest.mock import MagicMock, PropertyMock, patch

from autopytest.source import Source


@patch(
    "autopytest.source.Source.parent",
    new_callable=PropertyMock,
    return_value=Path("/usr/src/app"),
)
def test_should_build_regex_pattern(_mock: MagicMock) -> None:
    source = Source(directory="app", path=".")
    if platform.system() == "Windows":
        assert source.pattern == r"^D:/usr/src/app/app.+\.py$"
    else:
        assert source.pattern == r"^/usr/src/app/app.+\.py$"
