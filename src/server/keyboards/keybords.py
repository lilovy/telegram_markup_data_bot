from aiogram.types import (
    InlineKeyboardButton,
    KeyboardButton,
    Message,
)
from aiogram.utils.keyboard import (
    ReplyKeyboardBuilder,
    InlineKeyboardBuilder
)

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
