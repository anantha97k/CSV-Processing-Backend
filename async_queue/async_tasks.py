import asyncio
import csv


headers = [
    "UNIQUE_KEY",
    "PRODUCT_TITLE",
    "PRODUCT_DESCRIPTION",
    "SANMAR_MAINFRAME_COLOR",
    "SIZE",
    "COLOR_NAME",
    "PIECE_PRICE",
]


async def file_process(file, filename):
    # with open(f'{filename}', mode='wb') as tempfile:
    #     for line in file.readlines():
    #         line = line.decode('utf-8', errors='ignore').encode('utf-8')
    #         tempfile.write(line)
    # path = Path(filename)
    # return csv_parsing(path)
    await asyncio.sleep(2)
    return 0


def csv_parsing(path):

    with open(path, mode="r", newline="", encoding="utf-8") as csv_file:
        lines = csv.DictReader(csv_file)

        outer_list = []
        for line in lines:
            inner_list = []
            for r in headers:
                inner_list.append(f"({line[r]})")
            outer_list.append(tuple(inner_list))

    return outer_list
