from __future__ import annotations

from functools import partial
from typing import Any

from hermes_agent.config import AliceConfig
from hermes_agent.llm import LLMError, OpenAIChatClient
from hermes_agent.memory import ChatMemoryStore


START_TEXT = (
    "Hi, I am Alice. Send me a message and I will help. "
    "Use /help for commands or /reset to clear this chat history."
)

HELP_TEXT = "\n".join(
    [
        "Alice commands:",
        "/start - introduce Alice",
        "/help - show this help",
        "/reset - clear this chat history",
        "",
        "Configure your own .env locally. Do not send credentials in chat.",
    ]
)


async def handle_start(update: Any, context: Any) -> None:
    if update.message:
        await update.message.reply_text(START_TEXT)


async def handle_help(update: Any, context: Any) -> None:
    if update.message:
        await update.message.reply_text(HELP_TEXT)


async def handle_reset(
    update: Any, context: Any, memory: ChatMemoryStore
) -> None:
    if not update.message:
        return

    memory.reset(update.message.chat_id)
    await update.message.reply_text("Alice forgot this chat history.")


async def handle_text(
    update: Any,
    context: Any,
    memory: ChatMemoryStore,
    llm: OpenAIChatClient,
) -> None:
    if not update.message:
        return

    chat_id = update.message.chat_id
    text = (update.message.text or "").strip()
    if not text:
        await update.message.reply_text("Send me a text message and I will reply.")
        return

    memory.append(chat_id, "user", text)
    history = memory.get_history(chat_id)

    try:
        reply = llm.complete(history)
    except (LLMError, RuntimeError):
        await update.message.reply_text(
            "Alice could not reach the model provider. Check your local configuration."
        )
        return

    memory.append(chat_id, "assistant", reply)
    await update.message.reply_text(reply)


def build_application(config: AliceConfig):
    try:
        from telegram.ext import Application, CommandHandler, MessageHandler, filters
    except ImportError as exc:
        raise RuntimeError(
            "Missing dependency python-telegram-bot. Install the project first."
        ) from exc

    memory = ChatMemoryStore(config.memory_path, config.max_history_messages)
    llm = OpenAIChatClient(
        config.openai_api_key,
        config.openai_base_url,
        config.model,
    )

    app = Application.builder().token(config.telegram_bot_token).build()
    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(CommandHandler("help", handle_help))
    app.add_handler(CommandHandler("reset", partial(handle_reset, memory=memory)))
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            partial(handle_text, memory=memory, llm=llm),
        )
    )
    return app


def run_bot(config: AliceConfig) -> None:
    app = build_application(config)
    app.run_polling(allowed_updates=["message"])
