from aiogram import Router, F, types
from aiogram.types import Message, ContentType
from aiogram.methods import SendMessage
from aiogram.filters import Command
from aiogram.methods import (
    forward_message,
    send_message,
    )
from config import CHANNEL_ID

router = Router()

@router.message(Command(commands=["start"]))
async def welcome(msg: Message):
    await msg.answer('salem')


@router.message(Command(commands=['help']))
async def help(msg: Message):
    await msg.answer('bot for manual markup data')


@router.message(Command(commands=['reply']))
async def reply(msg: Message):
    await forward_message.ForwardMessage(chat_id=int(CHANNEL_ID), from_chat_id=msg.chat.id, message_id=msg.message_id)
    await send_message.SendMessage(chat_id=int(CHANNEL_ID), text='txt')


@router.message(F.text)
async def echo(message: types.Message):
    # Regular request, add bot: Bot to handler kwargs
    # await bot.send_message(message.chat.id, message.text)

    # or reply INTO webhook
    return SendMessage(chat_id=message.chat.id, text=message.text)