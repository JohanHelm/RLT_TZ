import os

import dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from app import DataAgregator

dotenv.load_dotenv()
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()


@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer("Бот готов к работе.")


@dp.message()
async def get_input_text(message: Message):
    data_agregator = DataAgregator(message.text)
    result_text = str(await data_agregator.execute())
    await message.answer(text=result_text)


async def start_bot():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
