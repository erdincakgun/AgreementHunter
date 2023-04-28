from sqlite3 import Error
import sqlite3


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect("records.db")
    except Error as e:
        print(e)

    if conn:
        return conn


def create_table(conn):
    table_query = """
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATETIME NOT NULL,
        record_file TEXT NOT NULL,
        transcript TEXT,
        aggreement_price INTEGER
    );
    """
    try:
        cursor = conn.cursor()
        cursor.execute(table_query)
    except Error as e:
        print(e)


def insert_record(conn, record):
    insert_query = """
    INSERT INTO records(date, record_file, transcript, aggreement_price)
    VALUES(?, ?, ?, ?)
    """

    cursor = conn.cursor()
    cursor.execute(insert_query, record)
    conn.commit()

    return cursor.lastrowid


def add_record(date, record_file, transcript, aggreement_price):
    connection = create_connection()
    record = (date, record_file, transcript, aggreement_price)
    record_id = insert_record(connection, record)

    return record_id


connection = create_connection()
create_table(connection)
