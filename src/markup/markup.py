from markupdata import GetFile, OpenFile, ParseData, SaveDoc, Create
from config import DATA_DIR
from ..db import action
import re


def create_record(
    filepath: str,
    record: str,
    ) -> None:
    save = SaveDoc(filepath)
    save.write(record)


def create_records(
    filepath: str,
    records: list,
    ) -> None:
    save = SaveDoc(filepath)
    for record in records:
        save.write(record)


def return_content(filepath: str):
    file = OpenFile(filepath)
    content = file.content
    
    return content


def get_file(file_id: str) -> list:
    files = GetFile(DATA_DIR).files
    for file in files:
        if file_id in file:
            return file
    return None


def get_user_tags(file_id: str) -> list:
    filepath = get_file(file_id)

    return return_content(filepath)


async def check_and_entry(
    user_id:int,
    project_name: str,
    file_id: str,
    limit: int = 100,
) -> None:
    """
    fill data to db
    
    Keyword arguments:
    user_id -- user identifier
    project_name -- name of project
    file_id -- file identifier
    limit -- download restriction
    """
    
    file = get_file(file_id)
    data = return_content(file)[:limit]
    if not await action.check_exist_data(
        user_id=user_id,
        project_name=project_name,
        ):
        await action.save_file_data(
            user_id=user_id,
            project_name=project_name,
            data=data,
            )


async def return_row(
    user_id: int,
    project_name: str,
) -> str:
    row = await action.get_data_row(
        user_id=user_id,
        project_name=project_name,
        )

    return await row


def pretty_row(
    header: str,
    row: str,
) -> str:
    sep = re.findall(r'[^\w\s]+', row)[0]
    row_s = row.split(sep=sep)
    header_s = header.split(sep=sep)
    pretty_list = list(zip(header_s, row_s))

    pretty_str = '\n'.join(f"{key}: {value}" for key, value in pretty_list)
    return pretty_str

