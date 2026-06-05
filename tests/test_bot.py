import unittest

from hermes_agent.bot import (
    HELP_TEXT,
    START_TEXT,
    handle_help,
    handle_reset,
    handle_start,
    handle_text,
)


class FakeMessage:
    def __init__(self, text, chat_id=123):
        self.text = text
        self.chat_id = chat_id
        self.replies = []

    async def reply_text(self, text):
        self.replies.append(text)


class FakeUpdate:
    def __init__(self, text, chat_id=123):
        self.message = FakeMessage(text, chat_id)


class FakeMemory:
    def __init__(self):
        self.history = {}
        self.appended = []
        self.reset_chat_ids = []

    def get_history(self, chat_id):
        return list(self.history.get(chat_id, []))

    def append(self, chat_id, role, content):
        self.appended.append((chat_id, role, content))
        self.history.setdefault(chat_id, []).append({"role": role, "content": content})

    def reset(self, chat_id):
        self.reset_chat_ids.append(chat_id)
        self.history.pop(chat_id, None)


class FakeLLM:
    def __init__(self, reply="Alice reply"):
        self.reply = reply
        self.histories = []

    def complete(self, history):
        self.histories.append(history)
        return self.reply


class BotHandlerTests(unittest.IsolatedAsyncioTestCase):
    async def test_start_replies_with_intro(self):
        update = FakeUpdate("/start")

        await handle_start(update, object())

        self.assertEqual(update.message.replies, [START_TEXT])

    async def test_help_replies_with_commands(self):
        update = FakeUpdate("/help")

        await handle_help(update, object())

        self.assertEqual(update.message.replies, [HELP_TEXT])

    async def test_reset_clears_chat_memory(self):
        update = FakeUpdate("/reset", chat_id=456)
        memory = FakeMemory()

        await handle_reset(update, object(), memory)

        self.assertEqual(memory.reset_chat_ids, [456])
        self.assertEqual(update.message.replies, ["Alice forgot this chat history."])

    async def test_empty_text_is_ignored_with_short_reply(self):
        update = FakeUpdate("   ", chat_id=123)
        memory = FakeMemory()
        llm = FakeLLM()

        await handle_text(update, object(), memory, llm)

        self.assertEqual(update.message.replies, ["Send me a text message and I will reply."])
        self.assertEqual(memory.appended, [])
        self.assertEqual(llm.histories, [])

    async def test_plain_text_updates_memory_and_replies(self):
        update = FakeUpdate("Hello", chat_id=123)
        memory = FakeMemory()
        llm = FakeLLM("Hi, I am Alice.")

        await handle_text(update, object(), memory, llm)

        self.assertEqual(
            memory.appended,
            [
                (123, "user", "Hello"),
                (123, "assistant", "Hi, I am Alice."),
            ],
        )
        self.assertEqual(llm.histories, [[{"role": "user", "content": "Hello"}]])
        self.assertEqual(update.message.replies, ["Hi, I am Alice."])

    async def test_model_errors_are_public_safe(self):
        class BrokenLLM:
            def complete(self, history):
                raise RuntimeError("private provider details")

        update = FakeUpdate("Hello", chat_id=123)
        memory = FakeMemory()

        await handle_text(update, object(), memory, BrokenLLM())

        self.assertEqual(
            update.message.replies,
            ["Alice could not reach the model provider. Check your local configuration."],
        )


if __name__ == "__main__":
    unittest.main()
