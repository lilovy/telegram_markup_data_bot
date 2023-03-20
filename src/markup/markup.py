from markupdata import GetFile, OpenFile, ParseData, SaveDoc, Create
from config import DATA_DIR
from ..db.action import get_data_row


def create_record(
    filepath: str,
    record: str,
    ) -> None:
    save = SaveDoc(filepath)
    save.write(record)


def return_record(filepath: str):
    file = OpenFile(filepath)
    content = file.content
    
    return content
