from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests

# توکن ربات تلگرام خود را اینجا قرار دهید
TELEGRAM_TOKEN = '7392446483:AAHrj5vuPQgYu9-zHnBlg77-7dJeo7yDUZY'

# آدرس API که در Flask ساخته‌اید
API_URL = 'http://127.0.0.1:5000/check_serial'

def start(update: Update, context: CallbackContext):
    update.message.reply_text('سلام! شماره سریال خود را ارسال کنید.')

def check_serial(update: Update, context: CallbackContext):
    serial_number = update.message.text

    # ارسال درخواست به API Flask
    response = requests.post(API_URL, json={'serial_number': serial_number})
    
    if response.status_code == 200:
        data = response.json()
        description = data.get('description', 'هیچ توضیحی پیدا نشد.')
        update.message.reply_text(f' کد ارسالی شما مربوط به کالای {description} میباشد')
    else:
        update.message.reply_text('شماره سریال پیدا نشد یا خطایی رخ داده است.')

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, check_serial))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
