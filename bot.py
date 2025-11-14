from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8431361772:AAFtxqvzhwblOJ2q7kSq-3urpiLG0wxdiHc"

# Start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🏠 Bosh sahifa", callback_data="home")],
        [InlineKeyboardButton("👤 About Me", callback_data="about")],
        [InlineKeyboardButton("📷 Gallery", callback_data="gallery")],
        [InlineKeyboardButton("🌐 Social", callback_data="social")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "✨ *Salom!* Men *Yosinxonning botiman*.\n\n"
        "Quyidagi tugmalardan tanlang va mini-saytga o‘xshash interaktiv bo‘limlarni ko‘ring:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Tugmalar uchun javob
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "home":
        await query.edit_message_text(
            "🏠 *Bosh sahifa*\n\n"
            "_Men Yosinxonning shaxsiy botiman. Men bilan interaktiv tarzda suhbatlashing va qiziqarli funksiyalardan foydalaning!_",
            parse_mode="Markdown"
        )

    elif query.data == "about":
        await query.edit_message_text(
            "👤 *About Me*\n\n"
            "*Ismim:* Yosinxon\n"
            "*Yoshim:* 18\n"
            "*Qiziqishlar:* IT, futbol, CS2, eFootball mobile va MLBB",
            parse_mode="Markdown"
        )

    elif query.data == "gallery":
        images = [
            "images/photo_2025-11-14_14-47-42.jpg",
            "images/photo_2025-11-14_14-47-57.jpg",
            "images/photo_2025-11-14_14-48-01.jpg",
            "images/photo_2025-11-14_14-48-04.jpg",
            "images/photo_2025-11-14_14-48-07.jpg"
        ]
        for img_path in images:
            with open(img_path, "rb") as img_file:
                await context.bot.send_photo(
                    chat_id=query.message.chat_id,
                    photo=img_file
                )
        await query.edit_message_text("✅ *Rasmlar ko‘rsatildi!*", parse_mode="Markdown")

    elif query.data == "social":
        keyboard = [
            [InlineKeyboardButton("📸 Instagram", url="https://www.instagram.com/rudy__o0/")],
            [InlineKeyboardButton("✉️ Telegram", url="https://t.me/Rudeus0")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🌐 *Ijtimoiy tarmoqlar:*",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()
