from aiogram.types import (
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import (
    ReplyKeyboardBuilder,
    InlineKeyboardBuilder
)


def get_keyboard_files(
    filenames: list[str],
    callback_text: str,
) -> InlineKeyboardBuilder():

    builder = InlineKeyboardBuilder()

    for filename in filenames:
        builder.add(
            InlineKeyboardButton(
                text=filename,
                callback_data=f"{callback_text}_{filename}",
                )
            )

    return builder
