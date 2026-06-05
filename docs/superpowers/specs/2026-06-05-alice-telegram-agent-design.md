# Alice Telegram Agent Design

## Goal

Build a public-safe Telegram AI agent named Alice. The repository must contain a
working template that other people can run with their own Telegram bot token and
OpenAI-compatible API credentials. The repository must not contain real tokens,
server details, chat IDs, runtime logs, sessions, cookies, databases, or local
environment files.

## Recommended Approach

Use a Python long-polling Telegram bot. This keeps the first public release easy
to run without a domain, HTTPS endpoint, or deployment-specific runbook. Users
will create a bot with BotFather, copy `.env.example` to `.env`, insert their own
values, install dependencies, and run the agent locally or on their own server.

Alternatives considered:

- Webhook bot: better for production hosting, but requires public HTTPS
  infrastructure and deployment-specific setup.
- Multi-integration bot: useful later, but too risky for the first release
  because each integration adds secret-handling and setup complexity.

## User Experience

Alice runs as a Telegram bot. A user sends messages in Telegram and receives
assistant replies. The bot supports:

- `/start`: introduce Alice and explain the minimal next action.
- `/help`: show available commands and configuration notes.
- `/reset`: clear the current chat's local conversation history.
- Plain text messages: send the current chat history to the configured model and
  return Alice's reply.

Alice's personality should be warm, concise, helpful, and practical. The prompt
will describe Alice at a design level only; it must not include private personal
details, private accounts, server coordinates, or operational history.

## Architecture

The project will be a small Python package:

- `hermes_agent/config.py`: load and validate environment variables.
- `hermes_agent/llm.py`: OpenAI-compatible chat completions client.
- `hermes_agent/memory.py`: bounded per-chat local conversation history.
- `hermes_agent/prompts.py`: public-safe Alice system prompt.
- `hermes_agent/bot.py`: Telegram command and message handlers.
- `hermes_agent/__main__.py`: CLI entry point.

Configuration will use placeholder examples only:

- `TELEGRAM_BOT_TOKEN`
- `OPENAI_API_KEY`
- `OPENAI_BASE_URL` for optional OpenAI-compatible providers
- `ALICE_MODEL`
- `ALICE_MEMORY_PATH`
- `ALICE_MAX_HISTORY_MESSAGES`

Runtime memory will be stored in a local JSON file whose default path is ignored
by git.

## Data Flow

1. Telegram sends an update to the polling bot.
2. The bot identifies the chat ID and message text.
3. Commands are handled locally.
4. Plain text messages are appended to bounded local memory.
5. The LLM client sends the Alice system prompt plus recent history to the
   configured OpenAI-compatible API.
6. Alice's reply is sent to Telegram and appended to memory.

## Error Handling

The agent should fail fast at startup when required environment variables are
missing. During runtime it should handle API and Telegram errors with concise
public-safe messages. It must not echo tokens, full environment values, stack
traces, server details, or provider secrets to users.

## Testing

Add focused tests for:

- config loading and validation;
- memory append, trimming, reset, and persistence behavior;
- LLM request payload construction with a fake transport or mocked client;
- bot command behavior where practical without requiring real Telegram or model
  credentials.

Before committing or pushing implementation changes, run:

- the Python test suite;
- `scripts/verify-no-secrets.ps1` on Windows.

## Public Safety

Only `.env.example` may be committed. Real `.env` files, runtime memory, logs,
sessions, credentials, hostnames, and deployment notes stay outside the public
repository. README instructions must use placeholders and design-level guidance
only.
