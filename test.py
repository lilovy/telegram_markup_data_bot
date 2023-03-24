# from src.db import action
# import asyncio


# async def run():
#     print(
#         await action.get_data_row(
#             user_id=653053151,
#             project_name='first',
#             )
#         )


# asyncio.run(run())



import markupdata

file = 'src\\data\\project_file\\653053151_word_def_BQACAgIAAxkBAAIGd2Qdeil-SbGCgZgjUqUNtLnOuQmtAAKaKAACSYvoSF16nwABgCdlGC8E.gz'
file = 'src\\data\\project_file\\653053151_first_marked.csv.gz'
file = 'src\\data\\project_file\\653053151_second_BQACAgIAAxkBAAIFEGQbJGTiESBVaUIfKhHPC1oIztnTAAJdLQACPevZSCfDzlKAzRVZLwQ.csv'
fl = markupdata.OpenFile(file)
print(fl.read())