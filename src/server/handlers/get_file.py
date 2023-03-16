import logging
from aiogram import Router, F
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.methods import (
    forward_message,
    send_message,
    send_document,
    get_file,
    )
from aiogram.client import bot

from ..keyboards.keybords import (
    get_keyboard_files,
    )
from ...db.action import (
    get_user_filenames,
    get_user_file,
    )
from ...db.models.async_models import File

router = Router()

@router.message(Command(commands=['getfile']))
async def get_file_info(msg: Message):
    await msg.answer(
        'Select a project',
        reply_markup=get_keyboard_files(
            filenames=await get_user_filenames(
                user_id=msg.chat.id,
                ),
            callback_text='get'
            ).as_markup(),
    )

@router.callback_query(Text(startswith='get_'))
async def send_user_file(callback: CallbackQuery):
    """
    return data from telegram cloud storage
    """
    filename = callback.data.split('_')[1]
    files = await get_user_file(
        user_id=callback.message.chat.id,
        project_name=filename,
        )
    await callback.message.answer(bot.GetFile(chat_id=files[0]))