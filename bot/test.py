import logging
import traceback

from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup,\
                                                ContentType
from aiogram.utils import exceptions
from aiogram.utils.executor import start_webhook
from aiogram import Bot, Dispatcher, types
from aiogram.bot import api
from aiogram.utils.json import json
from aiogram.utils.markdown import text


# API_TOKEN = "1056107759:AAHNMiYoq29h2yuXG35ukslmxgPCViQmMo4"
# PATCHED_URL = "https://telegg.ru/orig/bot{token}/{method}"
# setattr(api, 'API_URL', PATCHED_URL)

# webhook settings
WEBHOOK_HOST = 'https://52.47.187.186'
WEBHOOK_PATH = '/bot'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"


WEBHOOK_SSL_CERT = '/etc/nginx/ssl/nginx.crt'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = '/etc/nginx/ssl/nginx.key'  # Path to the ssl private key


# webserver settingsi
WEBAPP_HOST = '127.0.0.1'  # or ip
WEBAPP_PORT = 5000

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler()
async def echo(message: types.Message):
    # Regular request
    await bot.send_message(message.chat.id, message.text)

    # or reply INTO webhook
    # return SendMessage(message.chat.id, message.text)


async def on_startup(dp):
    web_hook = await bot.get_webhook_info()
    if web_hook.url != WEBHOOK_URL:
        if not web_hook.url:
            await bot.delete_webhook()
        # await bot.set_webhook(WEBHOOK_URL)
        await bot.set_webhook(WEBHOOK_URL, 
                                certificate=open(WEBHOOK_SSL_CERT, 'r'))
    print(await bot.get_webhook_info())
    # insert code here to run it after start


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
