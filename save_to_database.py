import sqlite3
import logging
import os

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

DATABASE_NAME = 'user_data.db'


def voices_db_init():
    try:
        sqliteConnection = sqlite3.connect(DATABASE_NAME)
        sqlite_create_table_query = """CREATE TABLE IF NOT EXISTS voices (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        user_id INTEGER NOT NULL,
                                        voice BLOB NOT NULL,
                                        created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                        FOREIGN KEY (user_id) REFERENCES user_data (id));"""
        cursor = sqliteConnection.cursor()
        logger.info("Successfuly Connected to SQLite")
        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        logger.info("SQLite VOICES table created")
        cursor.close()
    except sqlite3.Error as error:
        logger.info("Error while creating a sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            logger.info("sqlite connection is closed")


def db_init():
    try:
        sqliteConnection = sqlite3.connect(DATABASE_NAME)
        sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS user_data (
                                        id INTEGER PRIMARY KEY,
                                        photo BLOB NOT NULL);'''
        cursor = sqliteConnection.cursor()
        logger.info("Successfuly Connected to SQLite")
        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        logger.info("SQLite table created")
        cursor.close()
    except sqlite3.Error as error:
        logger.info("Error while creating a sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            logger.info("sqlite connection is closed")
            voices_db_init()


def convertToBinaryFile(filename):
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


def save_photo(user_id, img_path):
    db_init()
    try:
        sqliteConnection = sqlite3.connect(DATABASE_NAME)
        cursor = sqliteConnection.cursor()
        logger.info("Connected to SQLite")
        sqlite_insert_blob_query = """REPLACE INTO user_data(id, photo) VALUES(?, ?)"""
        user_photo = convertToBinaryFile(img_path)
        data_tuple = (user_id, user_photo)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        logger.info("Image and file inserted successfully as a BLOB into a table")
        cursor.close()
    except sqlite3.Error as error:
        logger.info("Failed to insert blob data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            logger.info("sqlite connection is closed")
            os.remove(img_path)


def save_voice(user_id, voice_path):
    db_init()
    try:
        sqliteConnection = sqlite3.connect(DATABASE_NAME)
        cursor = sqliteConnection.cursor()
        logger.info("Connected to SQLite")
        sqlite_insert_blob_query = """INSERT INTO voices(voice, user_id) VALUES(?, ?)"""
        user_voice = convertToBinaryFile(voice_path)
        cursor.execute(sqlite_insert_blob_query, (user_voice, user_id,))
        sqliteConnection.commit()
        logger.info("Voice inserted successfully as a BLOB into a table")
        cursor.close()
    except sqlite3.Error as error:
        logger.info("Failed to insert blob data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            logger.info("sqlite connection is closed")
            os.remove(voice_path)
