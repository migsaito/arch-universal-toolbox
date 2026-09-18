"""Application paths and user preferences."""

import json
from pathlib import Path
from typing import Any, Dict

APP_NAME = "arch-universal-toolbox"
CONFIG_DIR = Path.home() / ".config" / APP_NAME
CONFIG_FILE = CONFIG_DIR / "settings.json"


def load_settings() -> Dict[str, Any]:
    """Load settings, returning defaults when no file exists."""
    if not CONFIG_FILE.exists():
        return {"language": "en_US"}
    try:
        with CONFIG_FILE.open("r", encoding="utf-8") as stream:
            settings = json.load(stream)
    except (OSError, json.JSONDecodeError):
        return {"language": "en_US"}
    return settings if isinstance(settings, dict) else {"language": "en_US"}


def save_settings(settings: Dict[str, Any]) -> None:
    """Persist settings with private permissions."""
    CONFIG_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
    with CONFIG_FILE.open("w", encoding="utf-8") as stream:
        json.dump(settings, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
