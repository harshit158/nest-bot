import os
from dotenv import load_dotenv
load_dotenv()

from src.settings import settings

# observability setup should be done before importing any other modules that use logging or tracing
from foundry.observability import init_observability, ObservabilityConfig, get_logger, get_tracer
config = ObservabilityConfig(app_name=settings.app_name)
init_observability(config)

logger = get_logger(__name__)
tracer = get_tracer(__name__)

from src.agents import process_query

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler
)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with tracer.start_as_current_span("start_command"):
        logger.info(f"Received /start command from user: {update.effective_user.first_name} ({update.effective_user.id})")
        await update.message.reply_text(
            "Hello! 👋 I am your Telegram bot. Ask me anything!"
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show help\n\n"
        "You can also send me any message and I'll respond using an AI agent."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with tracer.start_as_current_span("handle_message"):
        logger.info(f"Received message: {update.message.text} from user: {update.effective_user.first_name} ({update.effective_user.id})")
        
        try:
            # Show typing indicator
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
            
            # Process query using the LangChain React agent
            response = process_query(update.message.text)
            
            # Send response back to user
            await update.message.reply_text(response)
        except Exception as e:
            logger.error(f"Error handling message: {str(e)}", exc_info=True)
            await update.message.reply_text(
                "Sorry, I encountered an error processing your request. Please try again."
            )

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    from telegram.ext import filters
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))  # Default handler for unknown messages

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
