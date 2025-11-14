from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os  # rasmlarni papkadan olish uchun

TOKEN = "8431361772:AAFtxqvzhwblOJ2q7kSq-3urpiLG0wxdiHc"

# Start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📄 About Me", callback_data="about")],
        [InlineKeyboardButton("🌐 Instagram", callback_data="instagram")],
        [InlineKeyboardButton("📷 Gallery", callback_data="gallery")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Salom! Men Yosinxonning botiman. Quyidagi tugmalardan tanlang:", 
        reply_markup=reply_markup
    )

# Tugmalar uchun javob
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "about":
        await query.edit_message_text(
            "👤 Ismim: Yosinxon\n🎂 Yoshim: 18\n💻 Qiziqish: IT, futbol, CS2, efootballmobile va MLBB"
        )
    elif query.data == "instagram":
        keyboard = [
            [InlineKeyboardButton("Instagram sahifam", url="https://www.instagram.com/rudy__o0/")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🌐 Instagram:", reply_markup=reply_markup)
    elif query.data == "gallery":
        images_folder = "images"  # hostingga yuklagan images papkang nomi
        try:
            for filename in sorted(os.listdir(images_folder)):
                if filename.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
                    with open(os.path.join(images_folder, filename), "rb") as f:
                        await context.bot.send_photo(chat_id=query.message.chat_id, photo=f)
            await query.edit_message_text("📷 Rasmlar ko‘rsatildi!")
        except Exception as e:
            await query.edit_message_text(f"❌ Rasmni yuklab bo‘lmadi: {e}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()
