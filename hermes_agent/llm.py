from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Protocol

from hermes_agent.prompts import ALICE_SYSTEM_PROMPT


class LLMError(RuntimeError):
    """Public-safe model provider error."""


class JsonTransport(Protocol):
    def post_json(
        self,
        url: str,
        headers: dict[str, str],
        payload: dict[str, Any],
        timeout: float,
    ) -> dict[str, Any]:
        raise NotImplementedError


class UrllibJsonTransport:
    def post_json(
        self,
        url: str,
        headers: dict[str, str],
        payload: dict[str, Any],
        timeout: float,
    ) -> dict[str, Any]:
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
        parsed = json.loads(body)
        if not isinstance(parsed, dict):
            raise ValueError("Expected JSON object response")
        return parsed


@dataclass
class OpenAIChatClient:
    api_key: str
    base_url: str
    model: str
    timeout: float = 30.0
    transport: JsonTransport | None = None

    def complete(self, history: list[dict[str, str]]) -> str:
        transport = self.transport or UrllibJsonTransport()
        try:
            response = transport.post_json(
                self._chat_completions_url(),
                self._headers(),
                self._payload(history),
                self.timeout,
            )
        except (OSError, ValueError, RuntimeError, urllib.error.URLError) as exc:
            raise LLMError("Could not reach the configured model provider.") from exc

        return self._extract_reply(response)

    def _chat_completions_url(self) -> str:
        return f"{self.base_url.rstrip('/')}/chat/completions"

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _payload(self, history: list[dict[str, str]]) -> dict[str, Any]:
        return {
            "model": self.model,
            "messages": [{"role": "system", "content": ALICE_SYSTEM_PROMPT}, *history],
        }

    @staticmethod
    def _extract_reply(response: dict[str, Any]) -> str:
        choices = response.get("choices")
        if not isinstance(choices, list) or not choices:
            raise LLMError("Model provider returned no reply.")

        first = choices[0]
        if not isinstance(first, dict):
            raise LLMError("Model provider returned no reply.")

        message = first.get("message")
        if not isinstance(message, dict):
            raise LLMError("Model provider returned no reply.")

        content = message.get("content")
        if not isinstance(content, str) or not content.strip():
            raise LLMError("Model provider returned no reply.")

        return content.strip()
