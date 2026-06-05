# Alice Telegram Agent

Alice is a public-safe Telegram AI agent template. It runs as a Telegram bot and
answers messages with an OpenAI-compatible chat completions provider.

This repository intentionally contains no real tokens, accounts, chat IDs,
server details, logs, sessions, databases, cookies, or local environment files.
Users bring their own credentials through a local `.env` file.

## What Alice Can Do

- Reply to Telegram text messages.
- Keep a small bounded local memory per Telegram chat.
- Clear a chat's memory with `/reset`.
- Work with OpenAI or another provider that supports the OpenAI chat
  completions API shape.

## Requirements

- Python 3.11 or newer.
- A Telegram bot token from BotFather.
- An OpenAI-compatible API key.

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the project:

```powershell
python -m pip install -e .
```

Copy the example environment file:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and replace placeholders with your own values:

```text
TELEGRAM_BOT_TOKEN=replace-with-your-telegram-bot-token
OPENAI_API_KEY=replace-with-your-openai-compatible-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
ALICE_MODEL=gpt-4o-mini
ALICE_MEMORY_PATH=.alice_memory.json
ALICE_MAX_HISTORY_MESSAGES=20
```

Never commit `.env`.

## Run

Start Alice with:

```powershell
python -m hermes_agent
```

Or use the installed script:

```powershell
alice-telegram-agent
```

Then open your Telegram bot and send a message.

## Telegram Commands

- `/start` introduces Alice.
- `/help` shows commands.
- `/reset` clears the current chat's local memory.

## Provider Notes

For OpenAI, keep:

```text
OPENAI_BASE_URL=https://api.openai.com/v1
```

For another OpenAI-compatible provider, set `OPENAI_BASE_URL` to that provider's
base API URL and choose a supported `ALICE_MODEL`. Do not put provider-specific
private details in this repository.

## Local Memory

Alice stores chat memory in `ALICE_MEMORY_PATH`, which defaults to
`.alice_memory.json`. The memory file is local runtime state and is ignored by
git.

## Tests

Run the test suite:

```powershell
python -m unittest discover -v
```

Before committing public changes, run the repository secret check:

```powershell
./scripts/verify-no-secrets.ps1
```

## Public Safety

This repository is a sanitized public workspace. Keep examples generic and use
placeholder values only. Do not commit real API keys, Telegram credentials,
OAuth credentials, SSH keys, cookies, sessions, logs, caches, databases, lock
files, runtime memory, or local environment files.
