import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# TOKENni env orqali oling (Railway uchun shunday bo'lishi kerak)
TOKEN = os.getenv("TOKEN", "YOUR_FALLBACK_TOKEN_IF_LOCAL")

# Rasm papkasi (bot.py joylashgan papkada 'images' papka bo'lsin)
IMAGE_FOLDER = os.path.join(os.getcwd(), "images")

# Oddiy in-memory settings (tekin saqlash, server qayta yuklanganda yo'qoladi)
user_settings = {}  # misol: {chat_id: {"notify": True}}

# --- Menyular ---
def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📄 About Me", callback_data="about")],
        [InlineKeyboardButton("🌐 Instagram", callback_data="instagram")],
        [InlineKeyboardButton("📷 Gallery", callback_data="gallery")],
        [InlineKeyboardButton("☎ Contact", callback_data="contact"),
         InlineKeyboardButton("⚙️ Settings", callback_data="settings")],
    ])

def instagram_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Open Instagram", url="https://www.instagram.com/rudy__o0/")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_main")]
    ])

def contact_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Message me", url="https://t.me/Dadalochka")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_main")]
    ])

def settings_keyboard(enabled: bool):
    label = "🔔 Notifications: ON" if enabled else "🔕 Notifications: OFF"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(label, callback_data="toggle_notify")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_main")]
    ])

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start — asosiy menyu"""
    text = ("Salom! Men Yosinxonning shaxsiy botiman. "
            "Quyidagi tugmalardan tanlang:")
    await update.message.reply_text(text, reply_markup=main_menu_keyboard())

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = (
        "/start — Asosiy menyu\n"
        "/help — Bu yordam xabari\n\n"
        "Menyudan About, Instagram, Gallery va Contactni ochishingiz mumkin."
    )
    await update.message.reply_text(txt)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """CallbackQuery handler — tugmalar bosilganda ishlaydi"""
    query = update.callback_query
    await query.answer()  # foydalanuvchiga "tayyor" signal

    data = query.data
    chat_id = query.message.chat_id

    # Main menu -> About
    if data == "about":
        await query.edit_message_text(
            "👤 Ismim: Yosinxon\n🎂 Yoshim: 18\n💻 Qiziqishlar: IT, futbol, CS2 ,efootballmobile va  MLBB",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_main")]])
        )

    # Instagram (ichki bo'lim — tugma orqali URL va Back)
    elif data == "instagram":
        await query.edit_message_text("🌐 Instagram:", reply_markup=instagram_keyboard())

    # Contact
    elif data == "contact":
        await query.edit_message_text("☎ Kontaktlar:", reply_markup=contact_keyboard())

    # Gallery — images papkasidagi barcha rasm fayllarini yuboradi
    elif data == "gallery":
        if not os.path.exists(IMAGE_FOLDER):
            await context.bot.send_message(chat_id=chat_id, text="Rasm papkasi topilmadi.")
            return

        files = sorted(os.listdir(IMAGE_FOLDER))
        image_extensions = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp")
        images = [f for f in files if f.lower().endswith(image_extensions)]
        if not images:
            await context.bot.send_message(chat_id=chat_id, text="Rasm topilmadi.")
            return

        # Avval eski xabarni yangilab "yuborilmoqda" deb ko'rsatamiz
        try:
            await query.edit_message_text("📷 Rasmlar yuborilmoqda...")
        except:
            pass

        # Rasmlarni ketma-ket yuborish
        for img in images:
            file_path = os.path.join(IMAGE_FOLDER, img)
            try:
                with open(file_path, "rb") as f:
                    await context.bot.send_photo(chat_id=chat_id, photo=f)
            except Exception as e:
                # agar bironta rasm yuborilmadi, foydalanuvchiga xabar beramiz
                await context.bot.send_message(chat_id=chat_id, text=f"Rasm yuborilmadi: {img}\n{e}")

        # Rasmlar tugagach asosiy menyuga qaytamiz (edit qila olsak)
        try:
            await context.bot.send_message(chat_id=chat_id, text="📷 Rasmlar ko‘rsatildi!", reply_markup=main_menu_keyboard())
        except:
            pass

    # Settings -> show current for this chat
    elif data == "settings":
        settings = user_settings.get(chat_id, {"notify": True})
        await query.edit_message_text("⚙️ Sozlamalar:", reply_markup=settings_keyboard(settings["notify"]))

    # Toggle notifications (oddiy misol)
    elif data == "toggle_notify":
        settings = user_settings.setdefault(chat_id, {"notify": True})
        settings["notify"] = not settings.get("notify", True)
        await query.edit_message_text("⚙️ Sozlamalar:", reply_markup=settings_keyboard(settings["notify"]))

    # Back to main menu
    elif data == "back_main":
        await query.edit_message_text("Asosiy menyu:", reply_markup=main_menu_keyboard())

    else:
        await query.edit_message_text("Noma'lum tugma, bosh menyuga qayting.", reply_markup=main_menu_keyboard())

# Simple error handler (log qiladi va foydalanuvchiga xabar beradi)
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    try:
        # send minimal message to user if possible
        if isinstance(update, Update) and update.effective_chat:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Xatolik yuz berdi, admin bilan bog'laning.")
    except:
        pass
    # hamma xatolikni console ga yozamiz
    print("Error:", context.error)

# --- App run ---
def main():
    if TOKEN in (None, "", "YOUR_FALLBACK_TOKEN_IF_LOCAL"):
        print("ERROR: TOKEN o'rnatilmagan. Railway da TOKEN env qo'yganingizga ishonch hosil qiling.")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_error_handler(error_handler)

    print("Bot ishga tushmoqda...")
    app.run_polling()

if __name__ == "__main__":
    main()
