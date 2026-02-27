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
    filters,
    ContextTypes,
    ConversationHandler,
)

BOT_TOKEN = "6301247571:AAGiFteJUSTpnMpgmIZKQc5EadMuhnU721o"
ADMIN_ID = 5590333379  # <-- Apna Telegram numeric ID

logging.basicConfig(level=logging.INFO)

# مراحل
FULLNAME, EMAIL, PHONE, ADDRESS = range(4)

# Countries List
countries = [
    "Pakistan", "India", "Bangladesh", "UAE", "Saudi Arabia",
    "Qatar", "Oman", "Turkey", "Malaysia", "Indonesia",
    "USA", "UK", "Canada", "Germany", "France",
    "Italy", "Spain", "Australia", "Brazil", "Japan"
]

plans = {
    "5GB - $10": "5GB - $10",
    "10GB - $18": "10GB - $18",
    "Unlimited - $35": "Unlimited - $35"
}


# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📦 View Plans", callback_data="menu")],
        [InlineKeyboardButton("ℹ️ About Us", callback_data="about")]
    ]
    text = (
        "🌟 *Welcome to Simart Data Entry Bot*\n\n"
        "We provide high-quality data packages worldwide.\n"
        "Trusted • Secure • Fast Delivery\n\n"
        "Please choose an option below:"
    )
    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# MENU
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = []
    for c in countries[:10]:
        keyboard.append([InlineKeyboardButton(c, callback_data=f"country_{c}")])

    keyboard.append([InlineKeyboardButton("➡️ More Countries", callback_data="more")])
    keyboard.append([InlineKeyboardButton("🔙 Back to Menu", callback_data="back_main")])

    await query.edit_message_text(
        "🌍 *Select Your Country:*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# MORE COUNTRIES
async def more(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = []
    for c in countries[10:]:
        keyboard.append([InlineKeyboardButton(c, callback_data=f"country_{c}")])

    keyboard.append([InlineKeyboardButton("🔙 Back to Menu", callback_data="back_main")])

    await query.edit_message_text(
        "🌍 *More Countries:*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# COUNTRY SELECT
async def country_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    country = query.data.split("_")[1]
    context.user_data["country"] = country

    keyboard = []
    for p in plans:
        keyboard.append([InlineKeyboardButton(p, callback_data=f"plan_{p}")])
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="menu")])

    await query.edit_message_text(
        f"📍 *{country} Plans:*\n\nSelect a plan:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# PLAN SELECT
async def plan_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    plan = query.data.replace("plan_", "")
    context.user_data["plan"] = plan

    await query.edit_message_text(
        "📝 *Please Enter Your Full Name:*",
        parse_mode="Markdown"
    )

    return FULLNAME


async def fullname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    if len(name) < 3:
        await update.message.reply_text(
            "⚠️ Please enter a valid full name."
        )
        return FULLNAME

    context.user_data["fullname"] = name
    await update.message.reply_text("📧 Enter Your Email Address:")
    return EMAIL


async def email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mail = update.message.text.strip()
    if "@" not in mail:
        await update.message.reply_text(
            "⚠️ Please enter a valid email address."
        )
        return EMAIL

    context.user_data["email"] = mail
    await update.message.reply_text("📱 Enter Your Phone Number:")
    return PHONE


async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text.strip()
    if len(phone) < 7:
        await update.message.reply_text(
            "⚠️ Please enter a valid phone number."
        )
        return PHONE

    context.user_data["phone"] = phone
    await update.message.reply_text("🏠 Enter Your Full Address:")
    return ADDRESS


async def address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    address = update.message.text.strip()
    if len(address) < 5:
        await update.message.reply_text(
            "⚠️ Please provide complete details correctly."
        )
        return ADDRESS

    context.user_data["address"] = address

    user = context.user_data

    admin_text = (
        "📥 *New Order Received*\n\n"
        f"👤 Name: {user['fullname']}\n"
        f"📧 Email: {user['email']}\n"
        f"📱 Phone: {user['phone']}\n"
        f"🏠 Address: {user['address']}\n"
        f"🌍 Country: {user['country']}\n"
        f"📦 Plan: {user['plan']}"
    )

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=admin_text,
        parse_mode="Markdown"
    )

    await update.message.reply_text(
        "✅ *Your request has been successfully sent!*\n\n"
        "Our admin team will contact you shortly for payment details.\n"
        "Please stay available.\n\n"
        "Thank you for trusting us 💙",
        parse_mode="Markdown"
    )

    return ConversationHandler.END


# ABOUT
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    text = (
        "🌟 *About Simart Data Entry*\n\n"
        "We are a trusted digital service provider offering secure and affordable data packages worldwide.\n\n"
        "✔ Fast Processing\n"
        "✔ 24/7 Support\n"
        "✔ Secure Transactions\n"
        "✔ Trusted by Many Clients\n\n"
        "Your satisfaction is our priority.\n"
        "Choose a plan today and experience premium service!"
    )

    keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back_main")]]

    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# BACK
async def back_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await start(query, context)


# MAIN
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(plan_select, pattern="^plan_")],
        states={
            FULLNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, fullname)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, email)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, phone)],
            ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, address)],
        },
        fallbacks=[]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(menu, pattern="menu"))
    app.add_handler(CallbackQueryHandler(more, pattern="more"))
    app.add_handler(CallbackQueryHandler(country_select, pattern="^country_"))
    app.add_handler(CallbackQueryHandler(about, pattern="about"))
    app.add_handler(CallbackQueryHandler(back_main, pattern="back_main"))
    app.add_handler(conv)

    app.run_polling()


if __name__ == "__main__":
    main()
