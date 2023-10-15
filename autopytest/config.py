import tomllib
from typing import Any

def parse_pyproject_toml(path: str) -> dict[str, Any]:
    with open(path, "rb") as f:
        pyproject_toml = tomllib.load(f)
    config: dict[str, Any] = pyproject_toml.get("tool", {}).get("autopytest", {})
    
    config.setdefault("pytest_args", [])
    config.setdefault("exclude_paths", [])
    config.setdefault("log_format", "%(message)s")
    config.setdefault("log_level", "INFO")
    
    return config
