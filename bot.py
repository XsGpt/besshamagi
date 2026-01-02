import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# --- BOT TOKEN ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN missing! Set it in Railway Variables.")

# --- ADMIN ID ---
ADMIN_ID = 7099421201  # Replace with your Telegram ID

# --- TEMPORARY CONFIG STORAGE ---
bot_config = {
    "description": "Welcome! Edit me with /setdescription",
    "links": {
        "google": "https://google.com",
        "desi": "https://www.xnxx.com/search/desi+mom+ki+chudai"
    },
    "profile_photo": None  # store file_id
}

# --- ADMIN CHECK ---
def is_admin(user_id):
    return user_id == ADMIN_ID

# --- /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"{bot_config['description']}\n"
    for name, url in bot_config['links'].items():
        text += f"{name.capitalize()} - {url}\n"
    if bot_config["profile_photo"]:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=bot_config["profile_photo"],
            caption=text
        )
    else:
        await update.message.reply_text(text)

# --- /setdescription ---
async def set_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ You are not allowed!")
        return
    if not context.args:
        await update.message.reply_text("Usage: /setdescription <text>")
        return
    bot_config["description"] = " ".join(context.args)
    await update.message.reply_text(f"✅ Description updated:\n{bot_config['description']}")

# --- /setlink ---
async def set_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ You are not allowed!")
        return
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /setlink <name> <url>")
        return
    name, url = context.args[0].lower(), context.args[1]
    bot_config["links"][name] = url
    await update.message.reply_text(f"✅ Link {name} set to {url}")

# --- /removelink ---
async def remove_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ You are not allowed!")
        return
    if not context.args:
        await update.message.reply_text("Usage: /removelink <name>")
        return
    name = context.args[0].lower()
    if name in bot_config["links"]:
        bot_config["links"].pop(name)
        await update.message.reply_text(f"✅ Link {name} removed")
    else:
        await update.message.reply_text(f"❌ No link found with name {name}")

# --- /showconfig ---
async def show_config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ You are not allowed!")
        return
    text = f"📝 Description: {bot_config['description']}\nLinks:\n"
    for name, url in bot_config["links"].items():
        text += f" - {name}: {url}\n"
    text += f"Profile photo: {'Set ✅' if bot_config['profile_photo'] else 'Not set ❌'}"
    await update.message.reply_text(text)

# --- /setphoto (via photo message) ---
async def set_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ You are not allowed!")
        return
    if not update.message.photo:
        await update.message.reply_text("Send a photo to set as profile pic.")
        return
    file_id = update.message.photo[-1].file_id  # highest resolution
    bot_config["profile_photo"] = file_id
    await update.message.reply_text("✅ Profile photo updated!")

# --- APP INIT ---
app = ApplicationBuilder().token(BOT_TOKEN).build()

# --- ADD HANDLERS ---
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("setdescription", set_description))
app.add_handler(CommandHandler("setlink", set_link))
app.add_handler(CommandHandler("removelink", remove_link))
app.add_handler(CommandHandler("showconfig", show_config))
app.add_handler(MessageHandler(filters.PHOTO & filters.User(ADMIN_ID), set_photo))

print("Bot running...")
app.run_polling()
