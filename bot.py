from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import random

TOKEN = "8431361772:AAFtxqvzhwblOJ2q7kSq-3urpiLG0wxdiHc"

# --- 2048 o'yin logikasi ---
def start_game():
    board = [[0]*4 for _ in range(4)]
    add_new_tile(board)
    add_new_tile(board)
    return board

def add_new_tile(board):
    empty = [(i,j) for i in range(4) for j in range(4) if board[i][j]==0]
    if empty:
        i,j = random.choice(empty)
        board[i][j] = random.choice([2,4])

def render_board(board):
    text = ""
    for row in board:
        text += " | ".join(str(num) if num!=0 else " " for num in row) + "\n"
    return f"```\n{text}```"

def transpose(board):
    return [list(row) for row in zip(*board)]

def reverse(board):
    return [row[::-1] for row in board]

def compress(row):
    new_row = [num for num in row if num!=0]
    new_row += [0]*(4-len(new_row))
    return new_row

def merge(row):
    for i in range(3):
        if row[i]==row[i+1] and row[i]!=0:
            row[i]*=2
            row[i+1]=0
    return row

def move_left(board):
    new_board=[]
    for row in board:
        row = compress(row)
        row = merge(row)
        row = compress(row)
        new_board.append(row)
    return new_board

def move_right(board):
    board = reverse(board)
    board = move_left(board)
    board = reverse(board)
    return board

def move_up(board):
    board = transpose(board)
    board = move_left(board)
    board = transpose(board)
    return board

def move_down(board):
    board = transpose(board)
    board = move_right(board)
    board = transpose(board)
    return board

# --- Mini-sayt tugmalari ---
def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🏠 Bosh sahifa", callback_data="home")],
        [InlineKeyboardButton("👤 About Me", callback_data="about")],
        [InlineKeyboardButton("📷 Gallery", callback_data="gallery")],
        [InlineKeyboardButton("🌐 Social", callback_data="social")],
        [InlineKeyboardButton("🎮 Games", callback_data="games")]
    ]
    return InlineKeyboardMarkup(keyboard)

# --- 2048 inline tugmalar ---
def game_keyboard():
    keyboard = [
        [InlineKeyboardButton("⬆️", callback_data="up")],
        [InlineKeyboardButton("⬅️", callback_data="left"),
         InlineKeyboardButton("➡️", callback_data="right")],
        [InlineKeyboardButton("⬇️", callback_data="down")],
        [InlineKeyboardButton("❌ Quit", callback_data="quit")]
    ]
    return InlineKeyboardMarkup(keyboard)

# --- Bot funksiyalari ---
games = {}  # chat_id: board

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = main_menu_keyboard()
    await update.message.reply_text(
        "✨ *Salom!* Men *Yosinxonning botiman*.\n\n"
        "Quyidagi tugmalardan tanlang va mini-saytga o‘xshash interaktiv bo‘limlarni ko‘ring:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id

    if query.data=="home":
        await query.edit_message_text(
            "🏠 *Bosh sahifa*\n\n"
            "_Men Yosinxonning shaxsiy botiman. Men bilan interaktiv tarzda suhbatlashing va qiziqarli funksiyalardan foydalaning!_",
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard()
        )
    elif query.data=="about":
        await query.edit_message_text(
            "👤 *About Me*\n\n"
            "*Ismim:* Yosinxon\n"
            "*Yoshim:* 18\n"
            "*Qiziqishlarim:* IT, futbol, CS2, eFootball mobile va MLBB",
            parse_mode="Markdown",
            reply_markup=main_menu_keyboard()
        )
    elif query.data=="gallery":
        images = [
            "images/photo_2025-11-14_14-47-42.jpg",
            "images/photo_2025-11-14_14-47-57.jpg",
            "images/photo_2025-11-14_14-48-01.jpg",
            "images/photo_2025-11-14_14-48-04.jpg",
            "images/photo_2025-11-14_14-48-07.jpg"
        ]
        for img_path in images:
            with open(img_path, "rb") as img_file:
                await context.bot.send_photo(chat_id=chat_id, photo=img_file)
        await query.edit_message_text("📷 *Rasmlar ko‘rsatildi!*", parse_mode="Markdown", reply_markup=main_menu_keyboard())

    elif query.data=="social":
        keyboard = [
            [InlineKeyboardButton("📸 Instagram", url="https://www.instagram.com/rudy__o0/")],
            [InlineKeyboardButton("✉️ Telegram", url="https://t.me/Rudeus0")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🌐 *Ijtimoiy tarmoqlar:*", reply_markup=reply_markup, parse_mode="Markdown")

    elif query.data=="games":
        board = start_game()
        games[chat_id] = board
        await query.edit_message_text("🎮 *2048 o'yinini boshladingiz!*", parse_mode="Markdown", reply_markup=game_keyboard())
        await context.bot.send_message(chat_id=chat_id, text=render_board(board), parse_mode="Markdown")

    elif query.data in ["up","down","left","right","quit"]:
        if chat_id not in games:
            games[chat_id] = start_game()
        board = games[chat_id]

        if query.data=="quit":
            games.pop(chat_id)
            await query.edit_message_text("❌ O'yin tugadi!", reply_markup=main_menu_keyboard())
            return

        if query.data=="up":
            board = move_up(board)
        elif query.data=="down":
            board = move_down(board)
        elif query.data=="left":
            board = move_left(board)
        elif query.data=="right":
            board = move_right(board)

        add_new_tile(board)
        games[chat_id] = board
        await query.edit_message_text(render_board(board), reply_markup=game_keyboard(), parse_mode="Markdown")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__=="__main__":
    main()
