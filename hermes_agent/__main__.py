from __future__ import annotations

from hermes_agent.bot import run_bot
from hermes_agent.config import ConfigError, load_config, load_dotenv_file


def main() -> int:
    load_dotenv_file()
    try:
        config = load_config()
    except ConfigError as exc:
        print(f"Configuration error: {exc}")
        return 2

    run_bot(config)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
