import re
from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    )
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, Text

from config import DATA_DIR
from ...db import action
from ..keyboards import keyboards
from ...markup import markup, checks
from ..init import bot


router = Router()


class MarkupData(StatesGroup):
    get_row = State()
    # stage2 = State()


def mimetype_to_type(mimetype: str) -> str:
    default_mime_types = {
            'text/plain': 'txt',
            'text/csv': 'csv',
            'application/gzip': 'gz'
        }
    return default_mime_types[mimetype]


@router.message(Command(commands=['start_markup']))
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
    await callback.message.delete()
    # await callback.message.answer('markup has begun')

    project_name = callback.data.split("___")[1]
    user_id = callback.message.chat.id

    await preprocessing(
        user_id=user_id,
        project_name=project_name,
    )

    await markup_data_row(
        msg=callback.message,
        state=state,
        user_id=user_id,
        project_name=project_name,
        )


async def markup_data_row(
    msg: Message,
    state: FSMContext,
    user_id: int,
    project_name: str,
):
    await state.clear()
    await state.set_state(MarkupData.get_row)

    row = await action.get_data_row(
        user_id=user_id,
        project_name=project_name,
        )
    
    if row:
        header = await action.get_header(
            user_id=user_id,
            project_name=project_name,
            )
        await state.update_data(
            user_id=user_id,
            project_name=project_name,
            row=row,
            tags='',
            )


        pretty_row = markup.pretty_row(
            row=row,
            header=header,
            )
        files_id = await action.get_user_file(
            user_id=user_id,
            project_name=project_name,
            )

        text = '*Select the desired tags*\ \n\n' + pretty_row

        await msg.answer(
            text=text,
            reply_markup=keyboards.get_keyboard_tags(
                tags=markup.get_user_tags(files_id[1]),
                ).as_markup(),
            parse_mode=ParseMode.MARKDOWN_V2,
            )
    
    else:
        await msg.answer('Marking complete!')


@router.callback_query(Text(startswith='TagsMarker_'))
async def send_user_file(
    callback: CallbackQuery, 
    state: FSMContext,
    ):

    tag = callback.data.split("___")[1]

    state_data = await state.get_data()
    row = state_data['row']

    # sep = re.findall(r'[^\w\s]+', row)[0]
    tags: str = tag + ',' + state_data['tags']

    await state.update_data(tags=tags)


@router.callback_query(Text('cancel_tags_markup'))
async def send_user_file(
    callback: CallbackQuery, 
    state: FSMContext,
    ):

    await callback.message.delete()
    await state.clear()
    await callback.message.answer('Canceled')


@router.callback_query(Text('confirm_and_next'))
async def send_user_file(
    callback: CallbackQuery, 
    state: FSMContext,
    ):

    await callback.message.delete()
    state_data = await state.get_data()

    user_id: int = state_data['user_id']
    project_name: str = state_data['project_name']
    tags: str = f"'{state_data['tags']}'"
    row: str = state_data['row']

    if tags != "''":
        await action.add_data_tags(
            user_id=user_id,
            project_name=project_name,
            row=row,
            tags=tags,
            )

        await markup_data_row(
            msg=callback.message,
            state=state,
            user_id=user_id,
            project_name=project_name,
            )
    
    await state.clear()

    await callback.answer('tags added', cache_time=2)


async def preprocessing(
    user_id: int,
    project_name: str,
    ) -> None:

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
        limit=100,
        )


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
        # res = await bot.get_file(file_id=file)
        f_type = mimetype_to_type(mimetype[i])
        destination = f'{DATA_DIR}{filename}.{f_type}'

        if not checks.check_file_exists(destination):
            await bot.download(
                file=file,
                destination=destination,
                )


