from aiogram import types
from app import dp


@dp.message_handler()
async def bot_echo(message: types.Message):
    await message.answer(message.text)
