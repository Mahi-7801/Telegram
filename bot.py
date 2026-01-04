
import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
AI_API_KEY = os.getenv("AI_API_KEY")

AI_API_URL = "https://api.groq.com/openai/v1/chat/completions"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Hello! Send me any message.")

def ai_reply(text):
    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": text}
        ]
    }

    r = requests.post(AI_API_URL, json=payload, headers=headers)

    if r.status_code == 200:
        return r.json()["choices"][0]["message"]["content"]

    return "AI error. Try again."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply = ai_reply(update.message.text)
    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
