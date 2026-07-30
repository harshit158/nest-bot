# Nest Bot

Nest Bot is a simple personal assistant project for everyday tasks. The goal is to build a lightweight helper that can support reminders, notes, small automations, and quick daily planning.

## What it does

- Starts a Telegram bot
- Responds to basic commands such as /start and /help
- Provides a simple foundation for future personal assistant features

## Roadmap

- Simple reminders and task prompts
- Notes and quick capture for daily thoughts
- Lightweight scheduling and routine support
- Small automations for common actions
- Better context-aware help over time

## Run locally

Set your Telegram token in the environment:

```bash
export TELEGRAM_BOT_TOKEN="your_token_here"
```

Build the project:

```bash
make build
```

Then start the app:

```bash
make run
```