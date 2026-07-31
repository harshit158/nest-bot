import os
from dotenv import load_dotenv
load_dotenv()

from src.settings import settings
from foundry.observability import init_observability, ObservabilityConfig, get_logger, get_tracer

config = ObservabilityConfig(app_name=settings.app_name)
init_observability(config)

logger = get_logger(__name__)
tracer = get_tracer(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    ConversationHandler
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with tracer.start_as_current_span("start_command"):
        logger.info(f"Received /start command from user: {update.effective_user.id}")
        await update.message.reply_text(
            "Hello! 👋 I am your Telegram bot."
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show help"
    )

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()