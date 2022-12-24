import sqlite3
import logging
import os

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

DATABASE_NAME = 'user_data.db'


def writeToFile(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)
    logger.info("Stored blob data into: ", filename, "\n")


def photo_from_db(user_id):
    temp_name = ""
    try:
        sqlite_connection = sqlite3.connect('user_data.db')
        cursor = sqlite_connection.cursor()
        logger.info("Successfuly Connected to SQLite")

        sql_fetch_blob_query = """SELECT * from user_data WHERE id = ?"""
        cursor.execute(sql_fetch_blob_query, (user_id,))
        record = cursor.fetchall()
        if record:
            temp_name = "temp_photo.jpg"
            for row in record:
                writeToFile(row[1], temp_name)
        cursor.close()
    except sqlite3.Error as error:
        logger.info("Failed to read blob data from sqlite table", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            logger.info("sqlite connection is closed")

    return temp_name


def voices_from_db(user_id):
    temp = list()
    try:
        sqlite_connection = sqlite3.connect('user_data.db')
        cursor = sqlite_connection.cursor()
        logger.info("Successfuly Connected to SQLite")
        sql_fetch_blob_query = """SELECT * from voices WHERE user_id = ?"""
        cursor.execute(sql_fetch_blob_query, (user_id,))
        record = cursor.fetchall()
        if record:
            for row in record:
                if not os.path.exists("temp_voices"):
                    os.mkdir("temp_voices")
                temp_file_name = "temp_voices/" + str(row[3]) + ".wav"
                writeToFile(row[2], temp_file_name)
                temp.append(temp_file_name)
        cursor.close()
    except sqlite3.Error as error:
        logger.info("Failed to read blob data from sqlite table", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            logger.info("sqlite connection is closed")

    return temp