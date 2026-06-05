from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping


DEFAULT_OPENAI_BASE_URL = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_MEMORY_PATH = Path(".alice_memory.json")
DEFAULT_MAX_HISTORY_MESSAGES = 20


class ConfigError(ValueError):
    """Raised when required Alice configuration is missing or invalid."""


@dataclass(frozen=True)
class AliceConfig:
    telegram_bot_token: str
    openai_api_key: str
    openai_base_url: str = DEFAULT_OPENAI_BASE_URL
    model: str = DEFAULT_MODEL
    memory_path: Path = DEFAULT_MEMORY_PATH
    max_history_messages: int = DEFAULT_MAX_HISTORY_MESSAGES


def load_dotenv_file(path: Path | str = ".env") -> None:
    env_path = Path(path)
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def load_config(env: Mapping[str, str] | None = None) -> AliceConfig:
    source = os.environ if env is None else env
    missing = [
        name
        for name in ("TELEGRAM_BOT_TOKEN", "OPENAI_API_KEY")
        if not source.get(name, "").strip()
    ]
    if missing:
        joined = ", ".join(missing)
        raise ConfigError(f"Missing required environment variables: {joined}")

    max_history_raw = source.get(
        "ALICE_MAX_HISTORY_MESSAGES", str(DEFAULT_MAX_HISTORY_MESSAGES)
    )
    try:
        max_history_messages = int(max_history_raw)
    except ValueError as exc:
        raise ConfigError("ALICE_MAX_HISTORY_MESSAGES must be an integer") from exc

    if max_history_messages < 1:
        raise ConfigError("ALICE_MAX_HISTORY_MESSAGES must be at least 1")

    return AliceConfig(
        telegram_bot_token=source["TELEGRAM_BOT_TOKEN"].strip(),
        openai_api_key=source["OPENAI_API_KEY"].strip(),
        openai_base_url=source.get("OPENAI_BASE_URL", DEFAULT_OPENAI_BASE_URL).strip()
        or DEFAULT_OPENAI_BASE_URL,
        model=source.get("ALICE_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL,
        memory_path=Path(
            source.get("ALICE_MEMORY_PATH", str(DEFAULT_MEMORY_PATH)).strip()
            or DEFAULT_MEMORY_PATH
        ),
        max_history_messages=max_history_messages,
    )
