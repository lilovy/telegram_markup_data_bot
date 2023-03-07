from aiogram import Router, F
from aiogram.types import Message, ContentType, CallbackQuery
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


@router.message(Command(commands=['return']))
async def return_message(msg: Message):
    
    await msg.answer(
        'Select a project',
        reply_markup=get_keyboard_files(
            filenames=await get_user_filenames(
                user_id=msg.chat.id,
                ),
            ).as_markup(),
    )


@router.callback_query(Text(startswith='return_'))
async def send_user_file(callback: CallbackQuery):
    filename = callback.data.split('_')[1]
    files = await get_user_file(
        user_id=callback.message.chat.id,
        projectname=filename,
        )
    await callback.message.answer_document(
        document=files[0],
        )
    await callback.message.answer_document(
        document=files[1],
        )

"""handler for save data in telegram cloud storage"""

# @router.message(F.document)
# async def save_document(msg: Message):
#     await msg.answer('save document...')
#     await forward_message.ForwardMessage(
#         chat_id=int(CHANNEL_ID),
#         from_chat_id=msg.chat.id,
#         message_id=msg.message_id,
#     )
#     await msg.answer('document saved!')