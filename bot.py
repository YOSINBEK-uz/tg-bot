import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8431361772:AAFtxqvzhwblOJ2q7kSq-3urpiLG0wxdiHc"  # BotFather'dan olingan token

# Rasm papkasi
IMAGE_FOLDER = os.path.join(os.getcwd(), "images")

# Start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📄 About Me", callback_data="about")],
        [InlineKeyboardButton("🌐 Instagram", callback_data="instagram")],
        [InlineKeyboardButton("📷 Gallery", callback_data="gallery")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Salom! Men shaxsiy botman. Quyidagi tugmalardan tanlang:", 
        reply_markup=reply_markup
    )

# Tugmalar uchun javob
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "about":
        await query.edit_message_text("👤 Ismim: Yosinxon\n🎂 Yoshim: 18\n💻 Qiziqish: IT, futbol, CS2 va MLBB")
    elif query.data == "instagram":
        keyboard = [
            [InlineKeyboardButton("Instagram sahifam", url="https://www.instagram.com/rudy__o0/")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🌐 Instagram:", reply_markup=reply_markup)
    elif query.data == "gallery":
        # IMAGE_FOLDER papkasidagi barcha rasm fayllarini yuborish
        if os.path.exists(IMAGE_FOLDER):
            files = os.listdir(IMAGE_FOLDER)
            photos_sent = 0
            for file in files:
                file_path = os.path.join(IMAGE_FOLDER, file)
                if os.path.isfile(file_path):
                    with open(file_path, "rb") as f:
                        await context.bot.send_photo(chat_id=query.message.chat_id, photo=f)
                    photos_sent += 1
            if photos_sent == 0:
                await context.bot.send_message(chat_id=query.message.chat_id, text="Rasmlar topilmadi.")
            else:
                await query.edit_message_text("📷 Rasmlar ko‘rsatildi!")
        else:
            await context.bot.send_message(chat_id=query.message.chat_id, text="Rasm papkasi topilmadi.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()
