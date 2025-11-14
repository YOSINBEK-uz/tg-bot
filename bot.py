from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = "8431361772:AAFtxqvzhwblOJ2q7kSq-3urpiLG0wxdiHc"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📄 About Me", callback_data="about")],
        [InlineKeyboardButton("🌐 Instagram", callback_data="instagram")],
        [InlineKeyboardButton("📷 Gallery", callback_data="gallery")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_text = (
        "👋 Salom, men Yosinxonning botiman!\n\n"
        "Quyidagi tugmalardan birini tanlab, men bilan tanishing:\n"
        "• 📄 About Me\n"
        "• 🌐 Instagram\n"
        "• 📷 Gallery"
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "about":
        about_text = (
            "👤 Ismim: Yosinxon\n"
            "🎂 Yoshim: 18\n"
            "💻 Qiziqishlar: IT, futbol, CS2,efootball mobile va MLBB\n"
            "📍 Joylashuv: Namangan shahar"
        )
        await query.edit_message_text(about_text)
    
    elif query.data == "instagram":
        keyboard = [[InlineKeyboardButton("📸 Instagram sahifam", url="https://www.instagram.com/rudy__o0/")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🌐 Men Instagramda ham kuzatishingiz mumkin:", reply_markup=reply_markup)

    elif query.data == "gallery":
        images_folder = "images"
        try:
            for filename in sorted(os.listdir(images_folder)):
                if filename.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
                    caption_text = f"🖼 Rasm: {filename}"
                    with open(os.path.join(images_folder, filename), "rb") as f:
                        await context.bot.send_photo(chat_id=query.message.chat_id, photo=f, caption=caption_text)
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
