from config import TOKEN
from aiogram import Bot
from aiogram.enums import ParseMode


bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
