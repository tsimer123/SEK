import sqlite3
import traceback
import sys
import datetime
from pathlib import Path

def sql_query_add_change_netinfo(data):

    db_dir = Path.cwd().parent
    db_dir = Path(db_dir, 'sqlite_python.db')
    now = datetime.datetime.now()
    data.append(now)
    try:
        sqlite_connection = sqlite3.connect(db_dir)
        cursor = sqlite_connection.cursor()

        sqlite_insert_query = f"""INSERT INTO changes_netinfo (ip, status, create_date, id_user) VALUES 
        ('{data[0]}', '{data[1]}', '{data[3]}', '{data[2]}');"""

        count = cursor.execute(sqlite_insert_query)
        sqlite_connection.commit()

        cursor.close()

    except sqlite3.Error as error:
        print("Не удалось вставить данные в таблицу sqlite")
        print("Класс исключения: ", error.__class__)
        print("Исключение", error.args)
        print("Печать подробноcтей исключения SQLite: ")
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            # print("Соединение с SQLite закрыто")

    return 1


def sql_write(sqlite_query):

    try:
        db_dir = Path.cwd().parent
        db_dir = Path(db_dir, 'sqlite_python.db')
        sqlite_connection = sqlite3.connect(db_dir)
        cursor = sqlite_connection.cursor()

        count = cursor.execute(sqlite_query)
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Не удалось вставить данные в таблицу sqlite")
        print("Класс исключения: ", error.__class__)
        print("Исключение", error.args)
        print("Печать подробноcтей исключения SQLite: ")
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            # print("Соединение с SQLite закрыто")

    return 1


def sql_query_select(sqlite_query):
    all_results = ''
    db_dir = Path.cwd().parent
    db_dir = Path(db_dir, 'sqlite_python.db')
    try:
        sqlite_connection = sqlite3.connect(db_dir)
        cursor = sqlite_connection.cursor()

        count = cursor.execute(sqlite_query)
        all_results = cursor.fetchall()
        cursor.close()

    except sqlite3.Error as error:
        print("Не удалось вставить данные в таблицу sqlite")
        print("Класс исключения: ", error.__class__)
        print("Исключение", error.args)
        print("Печать подробноcтей исключения SQLite: ")
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            # print("Соединение с SQLite закрыто")

    return all_results


def select_host_netinfo(host):

    sqlite_query = ''

    sqlite_query = (f"SELECT id FROM cli_networkinfo WHERE ip = '{host}';")

    return sqlite_query


def update_host_netinfo(id_host, data):

    now = datetime.datetime.now()
    data.append(now)

    sqlite_query = f"""UPDATE cli_networkinfo SET status_network = '{data[0]}', error = NULL, sourse_update = '{data[1]}', update_data = '{data[2]}' WHERE  id = '{id_host[0][0]}';"""

    return sqlite_query


def select_host_netinfo_all(host):

    sqlite_query = ''

    sqlite_query = (f"SELECT ip, channel, panid, status_network, error, sourse_update, update_data FROM cli_networkinfo WHERE ip = '{host}';")

    return sqlite_query