from aiogram import Router, F
from aiogram.types import (
    Message,
    ContentType,
    CallbackQuery,
    InputMediaDocument,
    )
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.methods import SendMessage
from aiogram.filters import Command, Text
from aiogram.methods import (
    forward_message,
    send_message,
    )

from config import CHANNEL_ID, DATA_DIR
from ...db import action
from ..keyboards import keyboards
from ...markup import markup, checks
from ..init import bot


router = Router()


class MarkupData(StatesGroup):
    stage1 = State()
    stage2 = State()


def mimetype_to_type(mimetype: str) -> str:
    default_mime_types = {
            'text/plain': 'txt',
            'text/csv': 'csv',
        }
    return default_mime_types[mimetype]


@router.message(Command(commands=['run']))
@router.message(F.text.casefold() == 'start markup')
async def start_project(msg: Message):
    await msg.answer(
        text="*Select a project*\ ",
        reply_markup=keyboards.get_keyboard_files(
            filenames=await action.get_user_filenames(
                user_id=msg.chat.id,
                ),
            callback_text='run',
            ).as_markup(),
        parse_mode=ParseMode.MARKDOWN_V2,
    )


@router.callback_query(Text(startswith='run_'))
async def run_select_project(
    callback: CallbackQuery,
    state: FSMContext,
    ):

    project_name = callback.data.split("_")[1]
    user_id = callback.message.chat.id

    await preprocessing(
        user_id=user_id,
        project_name=project_name,
    )

    await callback.message.answer(row)


async def markup_data_handler(
    msg: Message,
    state: FSMContext,
    ):
    await state.set_state(MarkupData.stage1)



@router.message(
    MarkupData.stage1,
    F.text
)


async def postprocessing():
    ...


async def preprocessing(
    user_id: int,
    project_name: str,
    ) -> tuple[str, str]:

    files = await action.get_user_file(
        user_id=user_id,
        project_name=project_name,
        )

    await download_select_project(
        user_id=user_id,
        project_name=project_name,
        files=files,
        )

    await markup.check_and_entry(
        user_id=user_id,
        project_name=project_name,
        file_id=files[0],
        )

    # row = await markup.return_row(
    #     user_id=user_id,
    #     project_name=project_name,
    #     )

    # return await (header, row)


async def download_select_project(
    user_id: int,
    project_name: str,
    files: list,
    ) -> None:

    mimetype = await action.get_file_mimetype(
        user_id=user_id,
        project_name=project_name,
        )

    for i, file in enumerate(files):
        
        filename = f'{user_id}_{project_name}_{file}'
        res = await bot.get_file(file_id=file)
        f_type = mimetype_to_type(mimetype[i])
        destination = f'{DATA_DIR}{filename}.{f_type}'

        if not checks.check_file_exists(destination):
            await bot.download(
                file=res,
                destination=destination,
                )


