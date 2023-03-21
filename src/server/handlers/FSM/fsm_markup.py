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
from ....db import action

router = Router()


class MarkupData(StatesGroup):
    stage1 = State()
    stage2 = State()


@router.message(Command(commands=['run']))
async def run_markup(msg: Message, state: FSMContext):
    await state.set_state(MarkupData.stage1)
    await msg.answer(text)