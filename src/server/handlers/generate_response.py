from aiogram import Router, F
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ParseMode
from aiogram.methods import (
    forward_message,
    send_message,
    send_document,
    get_file,
    )
from aiogram.client import bot

import gzip

from ..keyboards import keyboards
from ...db import action
from ...db.models.async_models import File
from ...markup import markup


router = Router()

@router.message(Command(commands=['get_response']))
@router.message(F.text.casefold() == 'get response')
async def return_response(msg: Message):
    # await msg.answer('The result is formed')
    await msg.answer(
        '*Select a project*\ ',
        reply_markup=keyboards.get_keyboard_result(
            projects=await action.get_user_filenames(
                user_id=msg.chat.id,
                ),
            callback_text='GetResult',
            ).as_markup(),
        parse_mode=ParseMode.MARKDOWN_V2,
    )


@router.callback_query(Text(startswith='GetResult___'))
async def send_response(callback: CallbackQuery):
    await callback.message.delete()

    project_name = callback.data.split('___')[1]
    await callback.message.answer('File generated')
    user_id = callback.message.chat.id
    
    filepath = await markup.report_generator(
        user_id=user_id,
        project_name=project_name,
        )
    
    file_Input = FSInputFile(filepath)
    # doc = gzip.open(filepath, 'rb')
    await callback.message.answer_document(
        document=file_Input,
        caption=f"Result for the project: *{project_name}*\ ",
        parse_mode=ParseMode.MARKDOWN_V2,
        )