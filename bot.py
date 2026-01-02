import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("8236616755:AAGW0hpPJAA3kOW15b3dCx8CI75Oe9pNB2I")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Google - https://google.com\nBingo - https://bingo.com"
    )

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
