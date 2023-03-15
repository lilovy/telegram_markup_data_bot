from aiogram import Router, F
from aiogram.types import (
    Message,
    ContentType,
    CallbackQuery,
    InputMediaDocument,
    )
from aiogram.enums import ParseMode
from aiogram.methods import SendMessage
from aiogram.filters import Command, Text
from aiogram.methods import (
    forward_message,
    send_message,
    )

from config import CHANNEL_ID
from ...db.action import (
    get_user_filenames,
    get_user_file,
    )
from ..keyboards.keybords import (
    get_keyboard_files,
    )
from ...markup.markup import *


router = Router()


@router.message(Command(commands=['run']))
async def start_project(msg: Message):
    await msg.answer(
        reply_markup=get_keyboard_files(
            filenames=await get_user_filenames(
                user_id=msg.chat.id,
                ),
            callback_text='run',
            ).as_markup(),
        parse_mode=ParseMode.MARKDOWN_V2,
    )


@router.callback_query(Text(startswith='run_'))
async def run_select_project(callback: CallbackQuery):
    ...


