import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("TOKEN")  # Render’dagi Environment Variable

# Rasmlar URL-larini GitHub repository-dan olamiz
IMAGES_BASE_URL = "https://raw.githubusercontent.com/YOSINBEK-uz/tg-bot/main/images/"

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
        await query.edit_message_text("👤 Ismim: Yosinxon\n🎂 Yoshim: 18\n💻 Qiziqish: IT, futbol, CS2 , efootballmobile va mlbb")
    elif query.data == "instagram":
        keyboard = [
            [InlineKeyboardButton("Instagram sahifam", url="https://www.instagram.com/rudy__o0/")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🌐 Instagram:", reply_markup=reply_markup)
    elif query.data == "gallery":
        # GitHub repository-dagi images papkasidagi barcha fayllarni avtomatik chiqarish
        import requests
        from bs4 import BeautifulSoup

        url = IMAGES_BASE_URL
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith(('.jpg', '.png', '.jpeg'))]
            for link in links:
                full_url = f"https://raw.githubusercontent.com/YOSINBEK-uz/tg-bot/main/images/{link.split('/')[-1]}"
                await context.bot.send_photo(chat_id=query.message.chat_id, photo=full_url)
            await query.edit_message_text("📷 Rasmlar ko‘rsatildi!")
        else:
            await query.edit_message_text("❌ Rasmlarni olishda xatolik yuz berdi.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()
