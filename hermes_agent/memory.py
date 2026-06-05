from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ChatMemoryStore:
    def __init__(self, path: Path | str, max_messages: int) -> None:
        if max_messages < 1:
            raise ValueError("max_messages must be at least 1")
        self.path = Path(path)
        self.max_messages = max_messages
        self._messages = self._load()

    def get_history(self, chat_id: int | str) -> list[dict[str, str]]:
        return list(self._messages.get(str(chat_id), []))

    def append(self, chat_id: int | str, role: str, content: str) -> None:
        chat_key = str(chat_id)
        history = self._messages.setdefault(chat_key, [])
        history.append({"role": role, "content": content})
        self._messages[chat_key] = history[-self.max_messages :]
        self._save()

    def reset(self, chat_id: int | str) -> None:
        self._messages.pop(str(chat_id), None)
        self._save()

    def _load(self) -> dict[str, list[dict[str, str]]]:
        if not self.path.exists():
            return {}

        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}

        if not isinstance(raw, dict):
            return {}

        loaded: dict[str, list[dict[str, str]]] = {}
        for chat_id, messages in raw.items():
            if not isinstance(chat_id, str) or not isinstance(messages, list):
                continue
            loaded[chat_id] = self._clean_messages(messages)[-self.max_messages :]
        return loaded

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(self._messages, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    @staticmethod
    def _clean_messages(messages: list[Any]) -> list[dict[str, str]]:
        cleaned: list[dict[str, str]] = []
        for message in messages:
            if not isinstance(message, dict):
                continue
            role = message.get("role")
            content = message.get("content")
            if isinstance(role, str) and isinstance(content, str):
                cleaned.append({"role": role, "content": content})
        return cleaned
