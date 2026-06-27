import os
import logging
import anthropic
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = "8204286096:AAHgS3Y6dvJH8nSTL7r7gSFqSzOzaob2qOI"
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

client = anthropic.Anthropic(api_key=ANTHROPIC_APISYSTEM_PROMPT = """Sen "Nemis Ustoz Bot" — o'zbek tilida gaplashadigan nemis tili o'qituvchisi botsan.
Faqat o'zbek tilida javob ber. Qisqa va qiziqarli o'qit. Emoji ishlat. Har javob oxirida keyingi qadam taklif qil."""

user_scores = {}
user_histories = {}async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_scores[user_id] = 0
    user_histories[user_id] = []
    await update.message.reply_text("🇩🇪 Nemis Ustoz Bot ga xush kelibsiz! Qayerdan boshlaysiz?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    if user_id not in user_histories:
        user_histories[user_id] = []
    user_histories[user_id].append({"role": "user", "content": text})
    recent = user_histories[user_id][-10:]
    try:
        response = client.messages.create(model="claude-sonnet-4-6", max_tokens=1000, system=SYSTEM_PROMPT, messages=recent)
        reply = response.content[0].text
        user_histories[user_id].append({"role": "assistant", "content": reply})
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("Xatolik yuz berdi.")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
