from aiogram.types import (
    InlineKeyboardButton,
    ReplyKeyboardMarkup, 
    KeyboardButton,
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

    return builder.adjust(3)


global_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text='Start'),
            KeyboardButton(text='Help'),
        ],
        [
            KeyboardButton(text='Add project'),
            KeyboardButton(text='Start markup'),
            # KeyboardButton(text='Cancel'),
        ],
    ],
)


markup_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            # KeyboardButton(text=)
        ]
    ]
)
