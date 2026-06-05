import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from hermes_agent.config import ConfigError, load_config, load_dotenv_file


class ConfigTests(unittest.TestCase):
    def test_loads_required_values_and_defaults(self):
        env = {
            "TELEGRAM_BOT_TOKEN": "telegram-token-placeholder",
            "OPENAI_API_KEY": "openai-key-placeholder",
        }

        config = load_config(env)

        self.assertEqual(config.telegram_bot_token, "telegram-token-placeholder")
        self.assertEqual(config.openai_api_key, "openai-key-placeholder")
        self.assertEqual(config.openai_base_url, "https://api.openai.com/v1")
        self.assertEqual(config.model, "gpt-4o-mini")
        self.assertEqual(config.memory_path, Path(".alice_memory.json"))
        self.assertEqual(config.max_history_messages, 20)

    def test_rejects_missing_required_values(self):
        with self.assertRaises(ConfigError) as error:
            load_config({})

        message = str(error.exception)
        self.assertIn("TELEGRAM_BOT_TOKEN", message)
        self.assertIn("OPENAI_API_KEY", message)

    def test_rejects_invalid_history_limit(self):
        env = {
            "TELEGRAM_BOT_TOKEN": "telegram-token-placeholder",
            "OPENAI_API_KEY": "openai-key-placeholder",
            "ALICE_MAX_HISTORY_MESSAGES": "zero",
        }

        with self.assertRaises(ConfigError) as error:
            load_config(env)

        self.assertIn("ALICE_MAX_HISTORY_MESSAGES", str(error.exception))

    def test_loads_dotenv_file_without_overwriting_existing_environment(self):
        with tempfile.TemporaryDirectory() as directory:
            env_path = Path(directory) / ".env"
            env_path.write_text(
                "\n".join(
                    [
                        "TELEGRAM_BOT_TOKEN=file-token",
                        "OPENAI_API_KEY=file-key",
                        "ALICE_MODEL=alice-model",
                    ]
                ),
                encoding="utf-8",
            )

            with patch.dict(os.environ, {"OPENAI_API_KEY": "existing-key"}, clear=True):
                load_dotenv_file(env_path)

                self.assertEqual(os.environ["TELEGRAM_BOT_TOKEN"], "file-token")
                self.assertEqual(os.environ["OPENAI_API_KEY"], "existing-key")
                self.assertEqual(os.environ["ALICE_MODEL"], "alice-model")

    def test_ignores_comments_and_blank_lines_in_dotenv_file(self):
        with tempfile.TemporaryDirectory() as directory:
            env_path = Path(directory) / ".env"
            env_path.write_text(
                "# comment\n\nTELEGRAM_BOT_TOKEN=telegram-token-placeholder\n",
                encoding="utf-8",
            )

            with patch.dict(os.environ, {}, clear=True):
                load_dotenv_file(env_path)

                self.assertEqual(
                    os.environ["TELEGRAM_BOT_TOKEN"], "telegram-token-placeholder"
                )


if __name__ == "__main__":
    unittest.main()
