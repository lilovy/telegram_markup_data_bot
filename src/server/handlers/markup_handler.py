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

from config import CHANNEL_ID, data_dir
from ...db.action import (
    get_user_filenames,
    get_user_file,
    get_file_mimetype,
    )
from ..keyboards.keybords import (
    get_keyboard_files,
    )
from ...markup.markup import *
from ..init import bot


router = Router()


def mimetype_to_type(mimetype: str) -> str:
    default_mime_types = {
            'text/plain': 'txt',
            'text/csv': 'csv',
        }
    return default_mime_types[mimetype]


@router.message(Command(commands=['run']))
async def start_project(msg: Message):
    await msg.answer(
        text="*Select a project*\ ",
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
    project_name = callback.data.split("_")[1]
    files = await get_user_file(
        user_id=callback.message.chat.id,
        project_name=filename,
        )
    mimetype = await get_file_mimetype(
        user_id=callback.message.chat.id,
        project_name=filename,
        )
    
    for i, file in enumerate(files):
        
        filename = project_name + '_' + file
        res = await bot.get_file(file_id=file)
        ftipe = mimetype_to_type(mimetype[i])
        await bot.download(
            file=res,
            destination=f'{data_dir}{filename}.{ftipe}',
            )
    await callback.message.answer('download complete')
    


