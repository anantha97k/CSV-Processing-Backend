import sqlite3


headers = [
"UNIQUE_KEY",
"PRODUCT_TITLE",
"PRODUCT_DESCRIPTION",
"SANMAR_MAINFRAME_COLOR",
"SIZE",
"COLOR_NAME",
"PIECE_PRICE"
]

table = '''
        CREATE TABLE IF NOT EXISTS file_data (
        UNIQUE_KEY INT PRIMARY KEY,
        PRODUCT_TITLE TEXT,
        PRODUCT_DESCRIPTION TEXT,
        SANMAR_MAINFRAME_COLOR TEXT,
        SIZE TEXT,
        COLOR_NAME TEXT,
        PIECE_PRICe REAL
    )
'''

insert = '''
        INSERT INTO file_data (UNIQUE_KEY, PRODUCT_TITLE, PRODUCT_DESCRIPTION, SANMAR_MAINFRAME_COLOR, SIZE, COLOR_NAME, PIECE_PRICE)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (UNIQUE_KEY) DO NOTHING

        ;           
'''

def db_insert(list):
    with sqlite3.connect("csv_processing.db") as connection:
        cursor = connection.cursor()

        cursor.executemany(insert, list)
        connection.commit()
    

def db_create():

    with sqlite3.connect("csv_processing.db") as connection:
        cursor = connection.cursor()
        cursor.execute(table)
