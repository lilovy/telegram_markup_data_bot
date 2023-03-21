from markupdata import GetFile, OpenFile, ParseData, SaveDoc, Create
from config import DATA_DIR
from ..db import action


def create_record(
    filepath: str,
    record: str,
    ) -> None:
    save = SaveDoc(filepath)
    save.write(record)


def return_content(filepath: str):
    file = OpenFile(filepath)
    content = file.content
    
    return content


def get_files(file_id: str) -> list:
    files = GetFile(DATA_DIR).files
    for file in files:
        if file_id in file:
            return file
    return None


# async def database_entry(
#     user_id: int,
#     project_name: str,
#     data: list,
# ):
#     await action.save_file_data(
#         user_id=user_id,
#         project_name=project_name,
#         data=data,
#         )


async def check_and_entry(
    user_id:int,
    project_name: str,
    file_id: str,
) -> None:
    file = get_files(file_id)
    data = return_content(file)
    if not await action.check_exist_data(
        user_id=user_id,
        project_name=project_name,
        ):
        await action.save_file_data(
            user_id=user_id,
            project_name=project_name,
            data=data,
            )

        # await database_entry(
        #     user_id=user_id,
        #     project_name=project_name, 
        #     data=data,
        #     )


async def return_row(
    user_id: int,
    project_name: str,
) -> str:
    row = await action.get_data_row(
        user_id=user_id,
        project_name=project_name,
        )
    await action.update_file_data_status(
        user_id=user_id,
        project_name=project_name,
        row=row,
        )


async def pretty_row(
    row: str,
) -> str:
    pty_row = ParseData(row)