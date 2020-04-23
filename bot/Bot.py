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

from parserKassir import *

API_TOKEN = "1056107759:AAHNMiYoq29h2yuXG35ukslmxgPCViQmMo4"

# webhook settings
WEBHOOK_HOST = '52.47.187.186'
WEBHOOK_PATH = '/bot'
WEBHOOK_URL = f"https://{WEBHOOK_HOST}{WEBHOOK_PATH}"

# Path to the ssl certificate
WEBHOOK_SSL_CERT = "nginx.crt"  # '/etc/nginx/ssl/nginx.crt'
# Path to the ssl private key
WEBHOOK_SSL_PRIV = "nginx.key"  # '/etc/nginx/ssl/nginx.key'

# webserver settings
WEBAPP_HOST = '127.0.0.1'  # or ip
WEBAPP_PORT = 5000

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

users_data = {}
users_pages = {}
user_favorite = {}

# Buttons
button_prev = InlineKeyboardButton("⬅", callback_data="button_prev")
button_next = InlineKeyboardButton("➡", callback_data="button_next")
button_details = InlineKeyboardButton("Подробнее",\
                                    callback_data="button_details")
button_buy = InlineKeyboardButton("Купить", callback_data="button_buy")
button_back = InlineKeyboardButton("Назад", callback_data="button_back")

# Markups
markup_product = InlineKeyboardMarkup()
markup_product.row(button_prev, button_next)
markup_product.add(button_details)
markup_product.insert(button_buy)

markup_details = InlineKeyboardMarkup()
markup_details.add(button_back)
markup_details.add(button_buy)


async def search_product(message: types.Message):
    users_data[message.from_user.id] = parser_search(message.text)
    users_pages[message.from_user.id] = 0
    print(users_data[message.from_user.id][users_pages[message.from_user.id]])
    await send_product(message.from_user.id)


async def send_product(id):
    text = ''
    print('testsp')
    text = users_data[id][users_pages[id]][1]
    await bot.send_photo(id, users_data[id][users_pages[id]][0],
                         reply_markup=markup_product,
                         caption=text,
                         parse_mode="html")


# Answer to help
@dp.message_handler(commands=["help"])
async def help_message(message: types.Message):
    await message.answer(text="help1")


# Answer to main menu and search
@dp.message_handler(content_types=types.ContentType.TEXT)
async def echo(message: types.Message):
    if message.text == "Поиск":
        await message.answer("🔎 Просто отправьте боту название товара.")
    elif message.text == "Избранное":
        await message.answer("Избранное!!!")
    elif message.text == "!!!Предложение дня!!!":
        await message.answer("Предложение дня)!!!")
    elif message.text == "По Категориям":
        await message.answer("По Категориям!!!")
    elif message.text == "Купоны и скидки":
        await message.answer("Купоны и скидки!!!")
    elif message.text == "Настройки":
        await message.answer("Настройки!!!")
    else:
        if message.from_user.id in users_data:
            users_data.pop(message.from_user.id)
        await search_product(message)


# unknown message
@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(msg: types.Message):
    message_text = text("Я не знаю, что с этим делать."\ 
                        "\nНапоминаю, что есть команда /help")
    await msg.reply(ContentType)


@dp.callback_query_handler(text="button_next")
async def process_callback_next(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await press_next(callback_query.from_user, callback_query.message)


@dp.callback_query_handler(text="button_prev")
async def process_callback_next(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await press_prev(callback_query.from_user, callback_query.message)


@dp.callback_query_handler(text="button_details")
async def process_callback_next(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await press_details(callback_query.from_user, callback_query.message)


@dp.callback_query_handler(text="button_buy")
async def process_callback_next(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await press_buy(callback_query.from_user, callback_query.message)


@dp.callback_query_handler(text="button_back")
async def process_callback_next(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await press_back(callback_query.from_user, callback_query.message)


@dp.errors_handler(exception=exceptions.BadRequest)
async def tg_bot_api_error(update: types. Update,\
                            error: exceptions.BadRequest):
    print('telegram error', error, update.as_json())
    return True


@dp.errors_handler(exception=TimeoutError)
async def timeout_error(update: types.Update, error):
    print('timeout')
    return True


async def press_next(user, message):
    if users_pages[user.id] + 1 < len(users_data[user.id]):
        users_pages[user.id] += 1
        await send_product(user.id)
        await bot.delete_message(chat_id=user.id,\
                                    message_id=message.message_id)


async def press_prev(user, message):
    if users_pages[user.id] > 0:
        users_pages[user.id] -= 1
        await bot.delete_message(chat_id=user.id,\
                                    message_id=message.message_id)
        await send_product(user.id)


async def press_details(user, message):
    await bot.delete_message(chat_id=user.id, message_id=message.message_id)
    str2 = ''
    str2 = users_data[user.id][users_pages[user.id]][0]
    details = 'https://t.me/iv?url=' + str2 + '&rhash=1fded6a3c8b800'
    await bot.send_message(chat_id=user.id, text=str2,\
                        reply_markup=markup_details)


async def press_buy(user, message):
    pass


async def press_back(user, message):
    await send_product(user.id)


async def on_startup(dp):
    web_hook = await bot.get_webhook_info()
    if web_hook.url != WEBHOOK_URL:
        if not web_hook.url:
            await bot.delete_webhook()
        # await bot.set_webhook(WEBHOOK_URL)
        await bot.set_webhook(WEBHOOK_URL,\
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
    parse_cities()
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
