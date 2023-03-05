import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.methods import (
    forward_message,
    send_message,
    )

# from ...middleware.access import FullAccessMiddleware
from config import CHANNEL_ID

router = Router()


class SaveFile(StatesGroup):
    save_csv = State()
    save_txt = State()


@router.message(Command(commands=['run']))
async def start_save(msg: Message, state: FSMContext):
    await state.set_state(SaveFile.save_csv)
    await msg.answer('send me a csv document with the target data to start the markup')


@router.message(SaveFile.save_csv, F.document)
async def save_csv(msg: Message, state: FSMContext):
    await state.update_data(csv_file=msg.message_id)
    await msg.answer('OK. Now add a txt file with categories for markup')
    await state.set_state(SaveFile.save_txt)


@router.message(SaveFile.save_csv)
async def save_csv_incorrectly(msg: Message):
    await msg.answer('Please, send csv file, or print /cancel for exit')


@router.message(SaveFile.save_txt, F.document)
async def save_txt(msg: Message, state: FSMContext):
    user_data = await state.get_data()

    #save csv file on private channel
    await msg.answer('saving csv file...')
    await forward_message.ForwardMessage(
        chat_id=int(CHANNEL_ID),
        from_chat_id=msg.chat.id,
        message_id=user_data['csv_file'],
    )
    await msg.answer('csv file saved')

    #save txt file on private channel
    await msg.answer('saving txt file...')
    await forward_message.ForwardMessage(
        chat_id=int(CHANNEL_ID),
        from_chat_id=msg.chat.id,
        message_id=msg.message_id,
    )
    await msg.answer('txt file saved')


@router.message(SaveFile.save_txt)
async def save_txt_incorrectly(msg: Message):
    await msg.answer('Please, send txt file, or print /cancel for exit')


@router.message(Command(commands=['cancel']))
@router.message(F.text.casefold() == 'cancel')
async def cancel_handler(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer('cancelled.')
