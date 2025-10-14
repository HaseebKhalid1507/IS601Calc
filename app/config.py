from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional


def _maybe_load_dotenv() -> None:
    """Optionally load .env if python-dotenv is available."""
    try:
        import importlib  # pylint: disable=import-outside-toplevel

        dotenv = importlib.import_module("dotenv")  # pragma: no cover
        load_dotenv = getattr(dotenv, "load_dotenv", None)  # pragma: no cover
        if callable(load_dotenv):  # pragma: no cover
            load_dotenv()  # pragma: no cover
    except ModuleNotFoundError:  # pragma: no cover - optional dependency
        pass


def _to_bool(value: Optional[str], default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    auto_save: bool = False
    csv_path: Optional[str] = None


def load_settings() -> Settings:
    """Load settings from environment with dotenv support.

    Recognized variables:
    - AUTO_SAVE: bool-like (1/true/yes/on)
    - HISTORY_CSV_PATH: filesystem path for CSV persistence
    """
    _maybe_load_dotenv()
    return Settings(
        auto_save=_to_bool(os.getenv("AUTO_SAVE"), default=False),
        csv_path=os.getenv("HISTORY_CSV_PATH"),
    )
