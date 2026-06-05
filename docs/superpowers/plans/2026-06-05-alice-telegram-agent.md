# Alice Telegram Agent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a public-safe Telegram AI agent named Alice that users can run with their own Telegram and OpenAI-compatible credentials.

**Architecture:** A small Python package loads local `.env` configuration, runs a long-polling Telegram bot, stores bounded per-chat memory in an ignored JSON file, and calls an OpenAI-compatible chat completions endpoint through a standard-library HTTP client. Tests avoid real Telegram and model credentials.

**Tech Stack:** Python 3.11+, `python-telegram-bot` for Telegram polling, Python standard library for config, memory, HTTP, and `unittest`.

---

### Task 1: Project Skeleton and Configuration

**Files:**
- Create: `pyproject.toml`
- Create: `.env.example`
- Modify: `.gitignore`
- Create: `hermes_agent/__init__.py`
- Create: `hermes_agent/config.py`
- Test: `tests/test_config.py`

- [ ] **Step 1: Write failing config tests**

Create tests that verify defaults, required values, integer parsing, and `.env` loading without real credentials.

- [ ] **Step 2: Run config tests and verify RED**

Run: `python -m unittest tests.test_config -v`
Expected: FAIL because `hermes_agent.config` does not exist.

- [ ] **Step 3: Implement config loader**

Implement `AliceConfig`, `ConfigError`, `load_dotenv_file`, and `load_config`.

- [ ] **Step 4: Run config tests and verify GREEN**

Run: `python -m unittest tests.test_config -v`
Expected: PASS.

### Task 2: Memory Store

**Files:**
- Create: `hermes_agent/memory.py`
- Test: `tests/test_memory.py`

- [ ] **Step 1: Write failing memory tests**

Cover append, trimming, loading invalid/missing files, per-chat isolation, and reset.

- [ ] **Step 2: Run memory tests and verify RED**

Run: `python -m unittest tests.test_memory -v`
Expected: FAIL because `hermes_agent.memory` does not exist.

- [ ] **Step 3: Implement memory store**

Implement `ChatMemoryStore` with JSON persistence and bounded history.

- [ ] **Step 4: Run memory tests and verify GREEN**

Run: `python -m unittest tests.test_memory -v`
Expected: PASS.

### Task 3: LLM Client and Alice Prompt

**Files:**
- Create: `hermes_agent/prompts.py`
- Create: `hermes_agent/llm.py`
- Test: `tests/test_llm.py`

- [ ] **Step 1: Write failing LLM tests**

Use a fake HTTP transport to verify payload, endpoint, authorization header, successful response parsing, and public-safe API error messages.

- [ ] **Step 2: Run LLM tests and verify RED**

Run: `python -m unittest tests.test_llm -v`
Expected: FAIL because `hermes_agent.llm` and `hermes_agent.prompts` do not exist.

- [ ] **Step 3: Implement prompt and client**

Implement a public-safe Alice prompt and an OpenAI-compatible chat completions client.

- [ ] **Step 4: Run LLM tests and verify GREEN**

Run: `python -m unittest tests.test_llm -v`
Expected: PASS.

### Task 4: Telegram Bot Runtime

**Files:**
- Create: `hermes_agent/bot.py`
- Create: `hermes_agent/__main__.py`
- Create: `tests/test_bot.py`

- [ ] **Step 1: Write failing bot handler tests**

Test `/start`, `/help`, `/reset`, empty text, and a plain-text message using fake update/context objects.

- [ ] **Step 2: Run bot tests and verify RED**

Run: `python -m unittest tests.test_bot -v`
Expected: FAIL because `hermes_agent.bot` does not exist.

- [ ] **Step 3: Implement bot handlers and entry point**

Implement handler functions, app builder, and `python -m hermes_agent`.

- [ ] **Step 4: Run bot tests and verify GREEN**

Run: `python -m unittest tests.test_bot -v`
Expected: PASS.

### Task 5: Documentation and Final Verification

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Update README**

Document setup with BotFather, `.env.example`, install, run, commands, memory, OpenAI-compatible providers, and public-safety notes using placeholders only.

- [ ] **Step 2: Run full verification**

Run:
- `python -m unittest discover -v`
- `./scripts/verify-no-secrets.ps1`
- `git status --short`

Expected: tests pass, no obvious secrets found, and only intended public files changed.

- [ ] **Step 3: Commit and push**

Stage only public-safe files, commit implementation, and push the current branch.
