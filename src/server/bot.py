import logging
import asyncio
from aiogram import Bot
from aiogram.types import Message
# from aiogram.utils.executor import start_webhook
# from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import Dispatcher
from config import TOKEN, ACCESS_ID, CHANNEL_ID
from src.server.middlewares import AccessMiddleware


logging.basicConfig(level=logging.INFO)
loop = asyncio.get_event_loop()

bot = Bot(token=TOKEN, loop=loop)
dp = Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(ACCESS_ID))


@dp.message_handler(commands=['start'])
async def welcome(msg: Message):
    await msg.answer('salem')


@dp.message_handler(commands='help')
async def help(msg: Message):
    await msg.answer('bot for manual markup data')


async def forward_message(msg: Message):
    await bot.forward_message(chat_id=int(CHANNEL_ID), from_chat_id=msg.chat.id, message_id=msg.message_id)


@dp.message_handler(commands='reply')
async def reply(msg: Message):
    await msg
    await bot.send_message(chat_id=int(CHANNEL_ID), text='text')


# async def on_startup(dp):
#     await bot.set_webhook(WEBHOOK_URL)


# async def on_shutdown(dp):
#     ...


# def main():
#     start_webhook(
#         dispatcher=dp, 
#         webhook_path=WEBHOOK_PATH, 
#         on_startup=on_startup, 
#         on_shutdown=on_shutdown,
#         skip_updates=True,
#         host=WEBAPP_HOST,
#         port=WEBAPP_PORT,
#         )
