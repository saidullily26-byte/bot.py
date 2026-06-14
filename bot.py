import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, 
    CommandHandler, 
    ContextTypes
)
import pyotp

# টোকেন ও কনফিগ (রেন্ডারের এনভায়রনমেন্ট ভেরিয়েবল থেকে)
BOT_TOKEN = os.getenv("8776265413:AAFovQKHmPVr8kqKRWfdl23e6_knkGkYzYk")
REQUIRED_CHANNEL = "https://t.me/+snA9FLnwDpc4ZjZl" # আপনার চ্যানেলের ইউজারনেম দিন

# লগিং সেটআপ
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def check_membership(user_id, context):
    try:
        member = await context.bot.get_chat_member(REQUIRED_CHANNEL, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if await check_membership(user_id, context):
        await update.message.reply_text("স্বাগতম! আপনি আমাদের মেম্বার। কোড পেতে /code কমান্ড দিন।")
    else:
        keyboard = [[InlineKeyboardButton("গ্রুপে জয়েন করুন", url=f"https://t.me/{REQUIRED_CHANNEL[1:]}")]]
        await update.message.reply_text("বট ব্যবহার করতে আগে আমাদের গ্রুপে জয়েন করুন:", reply_markup=InlineKeyboardMarkup(keyboard))

async def get_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if await check_membership(user_id, context):
        # এখানে আপনার সিক্রেট কী ব্যবহার করুন
        secret_key = os.getenv("SECRET_KEY") 
        if secret_key:
            totp = pyotp.TOTP(secret_key)
            code = totp.now()
            await update.message.reply_text(f"🔐 আপনার বর্তমান কোড: *`{code}`*", parse_mode='Markdown')
        else:
            await update.message.reply_text("এপিআই কনফিগার করা নেই।")
    else:
        await update.message.reply_text("আগে গ্রুপে জয়েন করুন!")

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('code', get_code))
    print("বট চলছে...")
    application.run_polling()
