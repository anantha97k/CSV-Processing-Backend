
import sqlite3, csv


headers = [
"UNIQUE_KEY",
"PRODUCT_TITLE",
"PRODUCT_DESCRIPTION",
"SANMAR_MAINFRAME_COLOR",
"SIZE",
"COLOR_NAME",
"PIECE_PRICE"
]


insert = '''
        INSERT INTO file_data (UNIQUE_KEY, PRODUCT_TITLE, PRODUCT_DESCRIPTION, SANMAR_MAINFRAME_COLOR, SIZE, COLOR_NAME, PIECE_PRICE)
        VALUES (?, ? , ? ,?, ? ,?, ?) 
        ON CONFLICT (UNIQUE_KEY) DO UPDATE SET
        PRODUCT_TITLE=excluded.PRODUCT_TITLE,
        PRODUCT_DESCRIPTION=excluded.PRODUCT_DESCRIPTION,
        SANMAR_MAINFRAME_COLOR=excluded.SANMAR_MAINFRAME_COLOR,
        SIZE=excluded.SIZE,
        COLOR_NAME=excluded.COLOR_NAME,
        PIECE_PRICE=excluded.PIECE_PRICE
        ;           
'''

    
def csv_parsing():

    with open('b.csv', mode='r', newline='', encoding='utf-8') as csv_file:
        line = csv.DictReader(csv_file)

        list  = []
        for l in line:
            inner_list = []
            for r in headers:
                  inner_list.append((l[r]))
            list.append(tuple(inner_list))
        
        return list[0:2]



with sqlite3.connect('csv_processing.db') as connection:
    cursor = connection.cursor()
    rows = cursor.execute('SELECT count(*) FROM file_data ')
    print(rows.fetchall())
