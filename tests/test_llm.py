import unittest

from hermes_agent.llm import LLMError, OpenAIChatClient
from hermes_agent.prompts import ALICE_SYSTEM_PROMPT


class FakeTransport:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def post_json(self, url, headers, payload, timeout):
        self.calls.append(
            {
                "url": url,
                "headers": headers,
                "payload": payload,
                "timeout": timeout,
            }
        )
        return self.response


class OpenAIChatClientTests(unittest.TestCase):
    def test_sends_openai_compatible_chat_completion_request(self):
        transport = FakeTransport(
            {"choices": [{"message": {"content": "Hello from Alice"}}]}
        )
        client = OpenAIChatClient(
            api_key="api-key-placeholder",
            base_url="https://example.test/v1/",
            model="alice-model",
            transport=transport,
        )

        reply = client.complete([{"role": "user", "content": "Hi"}])

        self.assertEqual(reply, "Hello from Alice")
        self.assertEqual(len(transport.calls), 1)
        call = transport.calls[0]
        self.assertEqual(call["url"], "https://example.test/v1/chat/completions")
        self.assertEqual(call["headers"]["Authorization"], "Bearer api-key-placeholder")
        self.assertEqual(call["headers"]["Content-Type"], "application/json")
        self.assertEqual(call["payload"]["model"], "alice-model")
        self.assertEqual(
            call["payload"]["messages"],
            [
                {"role": "system", "content": ALICE_SYSTEM_PROMPT},
                {"role": "user", "content": "Hi"},
            ],
        )

    def test_raises_public_safe_error_for_missing_choice(self):
        transport = FakeTransport({"choices": []})
        client = OpenAIChatClient(
            api_key="api-key-placeholder",
            base_url="https://example.test/v1",
            model="alice-model",
            transport=transport,
        )

        with self.assertRaises(LLMError) as error:
            client.complete([{"role": "user", "content": "Hi"}])

        self.assertEqual(str(error.exception), "Model provider returned no reply.")

    def test_raises_public_safe_error_for_transport_failure(self):
        class BrokenTransport:
            def post_json(self, url, headers, payload, timeout):
                raise RuntimeError("contains sensitive provider details")

        client = OpenAIChatClient(
            api_key="api-key-placeholder",
            base_url="https://example.test/v1",
            model="alice-model",
            transport=BrokenTransport(),
        )

        with self.assertRaises(LLMError) as error:
            client.complete([{"role": "user", "content": "Hi"}])

        self.assertEqual(
            str(error.exception), "Could not reach the configured model provider."
        )

    def test_prompt_is_public_safe(self):
        self.assertIn("Alice", ALICE_SYSTEM_PROMPT)
        forbidden = ["token", "ssh", "hostname", "chat id", "server coordinate"]
        lowered = ALICE_SYSTEM_PROMPT.lower()
        for word in forbidden:
            self.assertNotIn(word, lowered)


if __name__ == "__main__":
    unittest.main()
