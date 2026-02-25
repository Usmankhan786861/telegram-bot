import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from openpyxl import Workbook

import os
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# ========== MAIN MENU ==========
def main_menu():
    keyboard = [
        [InlineKeyboardButton("📝 Create Data Sheets", callback_data="create")],
        [InlineKeyboardButton("ℹ️ About", callback_data="about")],
        [InlineKeyboardButton("🆘 Help", callback_data="help")],
    ]
    return InlineKeyboardMarkup(keyboard)


# ========== SHEETS MENU ==========
def sheets_menu():
    keyboard = [
        [InlineKeyboardButton("📊 Individuals Sheet", callback_data="individuals")],
        [InlineKeyboardButton("📦 Products Data Sheet", callback_data="products")],
        [InlineKeyboardButton("🏢 Companies Data Sheet", callback_data="companies")],
        [InlineKeyboardButton("💼 Business Client Sheet", callback_data="business")],
        [InlineKeyboardButton("📈 Lead Generation Sheet", callback_data="lead")],
        [InlineKeyboardButton("📧 Email Marketing Sheet", callback_data="email")],
        [InlineKeyboardButton("📊 Sales Prospect Sheet", callback_data="sales")],
        [InlineKeyboardButton("💹 B2B Marketing Campaign Sheet", callback_data="b2b")],
        [InlineKeyboardButton("📂 CRM Data Sheet", callback_data="crm")],
        [InlineKeyboardButton("📅 Project Tracking Sheet", callback_data="project")],
        [InlineKeyboardButton("💻 Asset Management Sheet", callback_data="asset")],
        [InlineKeyboardButton("🧠 SWOT Analysis Sheet", callback_data="swot")],
        [InlineKeyboardButton("🔍 Market Research Sheet", callback_data="market")],
        [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="back")],
    ]
    return InlineKeyboardMarkup(keyboard)


# ========== START ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 *Smart Data Entry Bot*\n\nWelcome! Choose an option:",
        reply_markup=main_menu(),
        parse_mode="Markdown",
    )


# ========== BUTTON HANDLER ==========
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "create":
        await query.edit_message_text(
            "📂 Choose a Data Sheet:",
            reply_markup=sheets_menu(),
        )

    elif data == "about":
        await query.edit_message_text(
            "📊 Smart Data Entry Bot\n\n"
            "✔ Auto Excel Generator\n"
            "🎨 Fully Styled Sheets\n"
            "⚡ Fast • Easy • Professional\n\n"
            "Create clean Excel sheets in seconds!",
            reply_markup=main_menu(),
        )

    elif data == "help":
        await query.edit_message_text(
            "🆘 Help\n\n"
            "1️⃣ Select a sheet\n"
            "2️⃣ Enter data (comma separated)\n"
            "3️⃣ Receive Excel file instantly\n",
            reply_markup=main_menu(),
        )

    elif data == "back":
        await query.edit_message_text(
            "🏠 Main Menu:",
            reply_markup=main_menu(),
        )

    else:
        context.user_data["sheet_type"] = data
        await query.edit_message_text(
            f"✏️ Enter data for {data.capitalize()} Sheet (comma separated):\n\n"
            "Example:\nAli Khan, Sara Ahmed, Omar Riaz",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("⬅️ Back to Sheets Menu", callback_data="create")]]
            ),
        )


# ========== MESSAGE HANDLER ==========
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "sheet_type" not in context.user_data:
        return

    sheet_type = context.user_data["sheet_type"]
    user_input = update.message.text
    items = [item.strip() for item in user_input.split(",")]

    wb = Workbook()
    ws = wb.active
    ws.title = sheet_type.capitalize()

    ws.append([sheet_type.capitalize() + " Data"])

    for item in items:
        ws.append([item])

    file_name = f"{sheet_type}_sheet.xlsx"
    wb.save(file_name)

    await update.message.reply_document(document=open(file_name, "rb"))
    del context.user_data["sheet_type"]


# ========== MAIN ==========
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
