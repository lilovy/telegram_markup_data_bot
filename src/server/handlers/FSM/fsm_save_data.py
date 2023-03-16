from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.methods import (
    send_document,
    )

from config import CHANNEL_ID
from ...filters.filters import (
    UniqueFileName,
    MIMEType,
    access_mime_type,
    )
from ....db.action import (
    save_file_info,
    )

router = Router()


class SaveFile(StatesGroup):
    project_name = State()
    save_csv = State()
    save_txt = State()



def mimetype_to_type(mimetype: str) -> str:
    default_mime_types = {
            'text/plain': 'txt',
            'text/csv': 'csv',
        }
    return default_mime_types[mimetype]


@router.message(Command(commands=['cancel']))
@router.message(F.text.casefold() == 'cancel')
async def cancel_handler(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer('cancelled.')


@router.message(Command(commands=['add']))
async def start_save(msg: Message, state: FSMContext):
    await state.set_state(SaveFile.project_name)
    await msg.answer('enter name for project')
    

@router.message(
    SaveFile.project_name,
    F.text,
    UniqueFileName(),
    )
async def set_pj_name(msg: Message, name: str, state: FSMContext):
    name = name.replace(' ', '_')
    await state.update_data(name=name)
    await msg.answer(
        'Send a csv document\n' \
        'with the target data\n'
        )
    await state.set_state(SaveFile.save_csv)

@router.message(SaveFile.project_name)
async def set_pjname_incorrectly(msg: Message, state: FSMContext):
    await msg.answer(
        'Please set project name\n' \
        'or print /cancel for exit'
        )


@router.message(
    SaveFile.save_csv, 
    F.document,
    MIMEType(mime_access=access_mime_type['data']),
    )
async def save_csv(msg: Message, state: FSMContext):
    await state.update_data(csv_file=msg.document.file_id)
    await msg.answer(
        'OK. Now add a txt file\n' \
        'with categories for markup'
        )
    await state.set_state(SaveFile.save_txt)


@router.message(SaveFile.save_csv)
async def save_csv_incorrectly(msg: Message):
    await msg.answer(
        'Please, send csv file\n' \
        'or print /cancel for exit'
        )


@router.message(
    SaveFile.save_txt, 
    F.document,
    MIMEType(mime_access=access_mime_type['categories']),
    )
async def save_txt(msg: Message, state: FSMContext):
    user_data = await state.get_data()

    #save csv file on private channel
    await msg.answer('saving csv file...')
    await send_document.SendDocument(
        chat_id=CHANNEL_ID,
        document=user_data['csv_file']
    )

    await msg.answer('csv file saved')

    #save txt file on private channel
    await msg.answer('saving txt file...')
    await send_document.SendDocument(
        chat_id=CHANNEL_ID,
        document=msg.document.file_id,
    )

    await msg.answer('txt file saved')
    
    await save_file_info(
        user_id=msg.chat.id,
        name=user_data['name'], 
        id=user_data['csv_file'], 
        linked_file_id=msg.document.file_id,
        )

    state.clear()


@router.message(SaveFile.save_txt)
async def save_txt_incorrectly(msg: Message):
    await msg.answer(
        'Please, send txt file\n' \
        'or print /cancel for exit'
        )

