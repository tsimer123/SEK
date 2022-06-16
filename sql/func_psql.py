from variables import user_psql, pass_psql, host_psql, port_psql, database_psql
import psycopg2
from psycopg2 import Error


def sql_query_in_connect_db(sql_request):

    result = 1

    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(user=user_psql,
                                      # пароль, который указали при установке PostgreSQL
                                      password=pass_psql,
                                      host=host_psql,
                                      port=port_psql,
                                      database=database_psql)

        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        # Отправка запроса в БД
        cursor.execute(sql_request[1])
        # Запись измненией
        if sql_request[0] == 1:
            connection.commit()
        if sql_request[0] == 0:
            result = cursor.fetchall()

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            # print("Соединение с PostgreSQL закрыто")

    return result


def query_list_uspd():

    sql_request = []
    sql_request.append(0)  # select запросы без commit
    sql_request.append("select number_uspd, type_uspd, lat, long from uspd;")

    return sql_request


def query_list_meters(list_meters):
    if isinstance(list_meters, list):
        str_meters = ''
        for line_list_meters in list_meters:
            str_meters += "'"+line_list_meters+"', "
        str_meters = str_meters[:-2]

    else:
        str_meters = list_meters

    sql_request = []
    sql_request.append(0)  # select запросы без commit
    sql_request.append(f"""select number_meter, lat, long from meters where number_meter in ({str_meters});""")

    return sql_request



