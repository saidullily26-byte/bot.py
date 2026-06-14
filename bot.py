import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import pyotp

# এনভায়রনমেন্ট ভেরিয়েবল থেকে টোকেন নিন (নিরাপত্তার জন্য)
BOT_TOKEN = os.getenv("8776265413:AAFovQKHmPVr8kqKRWfdl23e6_knkGkYzYk")
REQUIRED_CHANNEL = "https://t.me/+snA9FLnwDpc4ZjZl" # আপনার চ্যানেলের ইউজারনেম

async def check_membership(user_id, context):
    try:
        member = await context.bot.get_chat_member(REQUIRED_CHANNEL, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if await check_membership(user_id, context):
        await update.message.reply_text("স্বাগতম! আপনি আমাদের মেম্বার। ২এফএ কোডের জন্য /code কমান্ড দিন।")
    else:
        keyboard = [[InlineKeyboardButton("গ্রুপে জয়েন করুন", url=f"https://t.me/{REQUIRED_CHANNEL[1:]}")]]
        await update.message.reply_text("বট ব্যবহার করতে আগে আমাদের গ্রুপে জয়েন করুন:", reply_markup=InlineKeyboardMarkup(keyboard))

async def code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # এখানে আপনার 2FA লজিক বসবে
    await update.message.reply_text("আপনার 2FA কোডটি এখানে জেনারেট হবে।")

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('code', code))
    application.run_polling()
