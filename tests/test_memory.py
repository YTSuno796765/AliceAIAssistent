import json
import tempfile
import unittest
from pathlib import Path

from hermes_agent.memory import ChatMemoryStore


class ChatMemoryStoreTests(unittest.TestCase):
    def test_appends_and_reads_messages_for_chat(self):
        with tempfile.TemporaryDirectory() as directory:
            store = ChatMemoryStore(Path(directory) / "memory.json", max_messages=4)

            store.append(123, "user", "hello")
            store.append(123, "assistant", "hi")

            self.assertEqual(
                store.get_history(123),
                [
                    {"role": "user", "content": "hello"},
                    {"role": "assistant", "content": "hi"},
                ],
            )

    def test_trims_oldest_messages_to_limit(self):
        with tempfile.TemporaryDirectory() as directory:
            store = ChatMemoryStore(Path(directory) / "memory.json", max_messages=3)

            store.append(123, "user", "one")
            store.append(123, "assistant", "two")
            store.append(123, "user", "three")
            store.append(123, "assistant", "four")

            self.assertEqual(
                store.get_history(123),
                [
                    {"role": "assistant", "content": "two"},
                    {"role": "user", "content": "three"},
                    {"role": "assistant", "content": "four"},
                ],
            )

    def test_keeps_chats_isolated(self):
        with tempfile.TemporaryDirectory() as directory:
            store = ChatMemoryStore(Path(directory) / "memory.json", max_messages=4)

            store.append(123, "user", "first")
            store.append(456, "user", "second")

            self.assertEqual(store.get_history(123), [{"role": "user", "content": "first"}])
            self.assertEqual(store.get_history(456), [{"role": "user", "content": "second"}])

    def test_persists_memory_to_disk(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "memory.json"

            first = ChatMemoryStore(path, max_messages=4)
            first.append(123, "user", "hello")

            second = ChatMemoryStore(path, max_messages=4)

            self.assertEqual(second.get_history(123), [{"role": "user", "content": "hello"}])

    def test_reset_clears_only_selected_chat(self):
        with tempfile.TemporaryDirectory() as directory:
            store = ChatMemoryStore(Path(directory) / "memory.json", max_messages=4)
            store.append(123, "user", "first")
            store.append(456, "user", "second")

            store.reset(123)

            self.assertEqual(store.get_history(123), [])
            self.assertEqual(store.get_history(456), [{"role": "user", "content": "second"}])

    def test_invalid_json_is_treated_as_empty_memory(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "memory.json"
            path.write_text("{not-json", encoding="utf-8")

            store = ChatMemoryStore(path, max_messages=4)

            self.assertEqual(store.get_history(123), [])

    def test_saved_file_uses_string_chat_ids(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "memory.json"
            store = ChatMemoryStore(path, max_messages=4)

            store.append(123, "user", "hello")

            saved = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(saved, {"123": [{"role": "user", "content": "hello"}]})


if __name__ == "__main__":
    unittest.main()
