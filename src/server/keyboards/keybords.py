from aiogram.types import (
    InlineKeyboardButton,
    KeyboardButton,
)
from aiogram.utils.keyboard import (
    ReplyKeyboardBuilder,
    InlineKeyboardBuilder
)
from aiogram.types import Message

# from ...db.action import get_user_filenames
from ...db.models.async_models import File


def get_keyboard_files(
    filenames: list[str],
) -> InlineKeyboardBuilder():

    builder = InlineKeyboardBuilder()

    for filename in filenames:
        builder.add(
            InlineKeyboardButton(
                text=filename,
                callback_data=f'return_{filename}',
                )
            )

    return builder
