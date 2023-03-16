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

router = Router()


@router.message(Command(commands=['projects']))
async def return_message(msg: Message):
    """
    return all projects of this user
    """
    await msg.answer(
        text="*Select a project*\ ",
        reply_markup=get_keyboard_files(
            filenames=await get_user_filenames(
                user_id=msg.chat.id,
                ),
            callback_text='return'
            ).as_markup(),
        parse_mode=ParseMode.MARKDOWN_V2
    )


@router.callback_query(Text(startswith='return_'))
async def send_user_file(callback: CallbackQuery):
    """
    return data from telegram cloud storage
    """
    filename = callback.data.split('_')[1]
    files = await get_user_file(
        user_id=callback.message.chat.id,
        project_name=filename,
        )
    
    # media_group = [
    #     InputMediaDocument(media=files[0]),
    #     InputMediaDocument(media=files[1]),
    # ]
    media_group = [
        InputMediaDocument(media=file)
        for file in files
    ]
    await callback.message.answer(
        f"*Project '{filename}':*\ ",
        parse_mode=ParseMode.MARKDOWN_V2)
    await callback.message.answer_media_group(
        media=media_group,
        )



