from aiogram import Router, F
from aiogram.types import Message, ContentType, CallbackQuery
from aiogram.methods import SendMessage
from aiogram.filters import Command, Text
from aiogram.methods import (
    forward_message,
    send_message,
    )
from ..keyboards import keyboards
from config import CHANNEL_ID

router = Router()

@router.message(Command(commands=["start"]))
@router.message(F.text.casefold() == 'start')
async def welcome(msg: Message):
    await msg.answer(
        'Hello!\n\n' \
        'this bot will help you to manually markup\n' \
        'data for neural network training\n\n' \
        'to start /add_project\n\n' \
        'for more information /help\n\n' \
        'contact @trump for full access',
        reply_markup=keyboards.global_keyboard,
        )


@router.message(Command(commands=['help']))
@router.message(F.text.casefold() == 'help')
async def help(msg: Message):
    await msg.answer('bot for manual markup data')


@router.message(Command(commands=['exit']))
@router.callback_query(Text('exit_from_files_keyboard'))
async def exit_handler(msg: CallbackQuery):
    await msg.message.delete()
    await msg.message.answer(
        "Start menu:",
        reply_markup=keyboards.global_keyboard,
        )
