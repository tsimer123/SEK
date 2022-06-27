from sql import func_psql
from excel import excel_func
from variables import header_dist
from yoda import yoda_func
import asyncio
import math
import datetime


# нужен был для тестов
async def coord_uspd_db_meter_user(meter_user):
    """
    Функция получает список из ПУ с его(их) координатами, запрашивает координаты УСПД из БД и передает эти данные для
    вычисления арстояния между ПУ и УСПД.
    Функция возаращетс сслку на Excel файл с результами работы.
    :param meter_user: список ПУ с координатами
    :return: ссылка на Excel файл на сервере с результатами работы функции
    """
    query_uspd = func_psql.query_list_uspd()
    list_uspd = func_psql.sql_query_in_connect_db(query_uspd)

    return math_uspd_meter(meter_user, list_uspd)


# мат функция по расчету растояния между координтами
def dist_calc_coordinates(list_coordinat):
    """
    Функция получает список из 2 координат [1 широта, 1 долгота, 2 широта, 2 долгота] и вычисляет растояние между 2
    точками на Земле по полученным координатм.
    Результатом выполнения функции является число float в км или сообщение об ошибке.
    :param list_coordinat: список из 4 значений соответвствуюзий 2 точками [1 широта, 1 долгота, 2 широта, 2 долгота]
    :return: число float в км или сообщение об ошибке
    """
    # pi - число pi, rad - радиус сферы (Земли)
    rad = 6372795

    # 55.662700, 38.017863
    # координаты двух точек
    try:
        llat1 = float(list_coordinat[0])
        llong1 = float(list_coordinat[1])
        llat2 = float(list_coordinat[2])
        llong2 = float(list_coordinat[3])

        # в радианах
        lat1 = llat1 * math.pi / 180.
        lat2 = llat2 * math.pi / 180.
        long1 = llong1 * math.pi / 180.
        long2 = llong2 * math.pi / 180.

        # косинусы и синусы широт и разницы долгот
        cl1 = math.cos(lat1)
        cl2 = math.cos(lat2)
        sl1 = math.sin(lat1)
        sl2 = math.sin(lat2)
        delta = long2 - long1
        cdelta = math.cos(delta)
        sdelta = math.sin(delta)

        # вычисления длины большого круга
        y = math.sqrt(math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
        x = sl1 * sl2 + cl1 * cl2 * cdelta
        ad = math.atan2(y, x)
        dist = ad * rad

        return dist / 1000

    except:
        # print(list_coordinat)
        return 'Не верный формат координат' + str(list_coordinat)


# получает одну элемент ОО и один ПУ и отправляет в мат функцию (отсеивает растояние больше 10 км)
def math_dist_one_meter(uspd, meter):
    """
    Функция получает список из УСПД и ПУ с коориатами и передает их в
    функцию для расчтеа растояния мужду ними, оцениват полученное растояние и если оно меньше 10 км то возращается
    список с растоянием если меньше то возращается int 0.
    :param uspd: [№ УСПД, широта, долгота]
    :param meter: [№ ПУ, широта, долгота]
    :return: Список с рузультатом либо int 0
    """

    list_coordinat = [uspd[2], uspd[3], meter[1], meter[2]]
    dist = dist_calc_coordinates(list_coordinat)
    if isinstance(dist, float):
        if dist < 10:  # max distance from uspd to meter
            list_one_meter = [meter[0], uspd[0], uspd[1], meter[1], meter[2], uspd[2], uspd[3], dist]
        else:
            list_one_meter = 0
    else:
        list_one_meter = [meter[0], uspd[0], uspd[1], meter[1], meter[2], uspd[2], uspd[3], 0, dist]

    return list_one_meter


# получает список УСПД и ПУ на выходе строка или файл с ближайшим ОО
def math_one_uspd_meter(type_mesg, meter_user, list_uspd):
    """
    Функция получает список прибоов учета (ПУ) и УСПД, для каждого ПУ отсеивается из списка УСПД, которые нахоядтся
    на растоянии до 10 км до ПУ.
    Функция возвращает ссылку на Excel файл с результатами.
    :param meter_user: список к ПУ (№ ПУ, широта, долгота)
    :param list_uspd: список с УСПД (№ УСПД, широта, долгота)
    :return: ссылка на Excel файл на сервере с результатами работы функции
    """
    list_dist = []

    for line_meter in meter_user:
        print(str(datetime.datetime.now()) + str(line_meter))
        list_dist_temp = []
        for line_uspd in list_uspd:
            list_one_meter = math_dist_one_meter(line_uspd, line_meter)
            if isinstance(list_one_meter, list):
                if len(list_one_meter) > 9:
                    list_dist_temp.append(
                        [line_meter[0], line_uspd[0], line_uspd[1], line_meter[1], line_meter[2], line_uspd[1], line_uspd[2], '',
                         'Не верный формат координат'])
                    break
            if list_one_meter != 0:
                list_dist_temp.append(list_one_meter)
        if len(list_dist_temp) > 0:
            list_dist_temp.sort(key=lambda x: x[6])
        else:
            list_dist_temp.append([line_meter[0], '-', '-', line_meter[1], line_meter[2], '', '', '',
                                   'В радиусе 10 км нет опорного оборудования'])

        list_dist.append(list(list_dist_temp[0]))

        list_dist_temp.clear()

    i = 1
    for line_list_dist in list_dist:
        line_list_dist.insert(0, i)
        i += 1

    if type_mesg == 'file':
        return list_dist
        # return excel_func.save_data_excel_in_wb(list_dist, 'dist', header_dist)
    if type_mesg == 'str':
        result_out_str = ''
        for line_list_dist in list_dist:
            if len(line_list_dist) < 10:
                result_out_str += line_list_dist[1] + ' - ' + line_list_dist[2] + ' - ' + line_list_dist[3] + ' - ' + str(round(line_list_dist[8], 4)) + 'км\n'
            if len(line_list_dist) == 10:
                result_out_str += line_list_dist[1] + ' - ' + line_list_dist[9] + '\n'
        return result_out_str


# находит разницу между ПУ из запроса и ответа в БД
def dif_list(list_1, list_2):

    dif_1 = set(list_1).difference(set(list_2))
    dif_2 = set(list_2).difference(set(list_1))

    list_dif = list(dif_1.union(dif_2))

    return list_dif


# находит все успд в радиусе 10 км от ПУ
def math_uspd_meter(meter_user, list_uspd):
    """
    Функция получает список прибоов учета (ПУ) и УСПД, для каждого ПУ отсеивается из списка УСПД, которые нахоядтся
    на растоянии до 10 км до ПУ.
    Функция возвращает ссылку на Excel файл с результатами.
    :param meter_user: список к ПУ (№ ПУ, широта, долгота)
    :param list_uspd: список с УСПД (№ УСПД, широта, долгота)
    :return: ссылка на Excel файл на сервере с результатами работы функции
    """
    list_dist = []

    for line_meter in meter_user:
        list_dist_temp = []
        for line_uspd in list_uspd:
            list_one_meter = math_dist_one_meter(line_uspd, line_meter)
            if isinstance(list_one_meter, list):
                if len(list_one_meter) > 9:
                    list_dist_temp.append(
                        [line_meter[0], line_uspd[0], line_meter[1], line_meter[2], line_uspd[1], line_uspd[2], '',
                         'Не верный формат координат'])
                    break
            if list_one_meter != 0:
                list_dist_temp.append(list_one_meter)
        if len(list_dist_temp) > 0:
            list_dist_temp.sort(key=lambda x: x[6])
        else:
            list_dist_temp.append([line_meter[0], '-', line_meter[1], line_meter[2], '', '', '',
                                   'В радиусе 10 км нет опорного оборудования'])

        for line_list_dist_temp in list_dist_temp:
            list_dist.append(list(line_list_dist_temp))

        list_dist_temp.clear()

    i = 1
    for line_list_dist in list_dist:
        line_list_dist.insert(0, i)
        i += 1

    # return excel_func.save_data_excel_in_wb(list_dist, 'dist', header_dist)
    return list_dist


# coorddb_nums вернет все УСПД в радиусе 10км для ПУ из БД
async def coord_uspd_db_num_meters_user(list_meters):

    query_uspd = func_psql.query_list_uspd()
    list_uspd = func_psql.sql_query_in_connect_db(query_uspd)

    query_meters = func_psql.query_list_meters(list_meters)
    list_meters_db = func_psql.sql_query_in_connect_db(query_meters)

    if len(list_meters) > 0:
        temp_list_meter = []
        for line_list_meters_db in list_meters_db:
            temp_list_meter.append(line_list_meters_db[0])
        list_finish = math_uspd_meter(list_meters_db, list_uspd)
        list_dif = dif_list(list_meters, temp_list_meter)
        if len(list_dif) > 0:
            for line_list_dif in list_dif:
                i = len(list_finish) + 1
                line_temp_error_meter = [i, line_list_dif, '', '', '', '', '', '', '', 'ПУ нет в БД PNR_SEK_bot']
                list_finish.append(line_temp_error_meter)
        return excel_func.save_data_excel_in_wb(list_finish, 'dist', header_dist)
    else:
        list_error = ['В БД @PNR_SEK_bot нет ни одного ПУ с таким(и) номером(ами)']
        return list_error


# coordBD_num_f - возвращает ближайшую УСПД для списка ПУ в формате файла
async def coord_uspd_db_one_meter_user_file(list_meters):

    query_uspd = func_psql.query_list_uspd()
    list_uspd = func_psql.sql_query_in_connect_db(query_uspd)

    query_meters = func_psql.query_list_meters(list_meters)
    list_meters_db = func_psql.sql_query_in_connect_db(query_meters)

    if len(list_meters) > 0:
        temp_list_meter = []
        for line_list_meters_db in list_meters_db:
            temp_list_meter.append(line_list_meters_db[0])
        list_finish = math_one_uspd_meter('file', list_meters_db, list_uspd)
        list_dif = dif_list(list_meters, temp_list_meter)
        if len(list_dif) > 0:
            for line_list_dif in list_dif:
                i = len(list_finish) + 1
                line_temp_error_meter = [i, line_list_dif, '', '',  '',  '',  '',  '',  '', 'ПУ нет в БД PNR_SEK_bot']
                list_finish.append(line_temp_error_meter)
        return excel_func.save_data_excel_in_wb(list_finish, 'dist', header_dist)
    else:
        list_error = ['В БД @PNR_SEK_bot нет ни одного ПУ с таким(и) номером(ами)']
        return list_error


# coordBD_num_s - возвращает ближайшую УСПД для списка ПУ в формате строке в сообщении
async def coord_uspd_db_one_meter_user_str(list_meters):

    query_uspd = func_psql.query_list_uspd()
    list_uspd = func_psql.sql_query_in_connect_db(query_uspd)

    query_meters = func_psql.query_list_meters(list_meters)
    list_meters_db = func_psql.sql_query_in_connect_db(query_meters)

    if len(list_meters_db) > 0:
        temp_list_meter = []
        for line_list_meters_db in list_meters_db:
            temp_list_meter.append(line_list_meters_db[0])
        list_finish = math_one_uspd_meter('str', list_meters_db, list_uspd)
        list_dif = dif_list(list_meters, temp_list_meter)
        if len(list_dif) > 0:
            for line_list_dif in list_dif:
                list_finish = list_finish + line_list_dif + ' - ПУ нет в БД @PNR_SEK_bot' + '\n'
        return list_finish
    else:
        list_error = ['В БД @PNR_SEK_bot нет ни одного ПУ с таким(и) номером(ами)']
        return list_error


# coord_ll_s - возвращает ближайшую УСПД по координатам пользователя в формате строке в сообщении
async def coord_uspd_db_coord_user_str(user_coords):

    query_uspd = func_psql.query_list_uspd()
    list_uspd = func_psql.sql_query_in_connect_db(query_uspd)

    list_user_coord = [[user_coords[0] + ' ' + user_coords[1], user_coords[0], user_coords[1]]]

    list_finish = math_one_uspd_meter('str', list_user_coord, list_uspd)

    return list_finish


# coord_ll_f - возвращает ближайшую УСПД по координатам пользователя в формате файла
async def coord_uspd_db_coord_user_file(user_coords):

    query_uspd = func_psql.query_list_uspd()
    list_uspd = func_psql.sql_query_in_connect_db(query_uspd)

    list_user_coord = [[user_coords[0] + ' ' + user_coords[1], user_coords[0], user_coords[1]]]

    list_finish = math_one_uspd_meter('file', list_user_coord, list_uspd)

    return excel_func.save_data_excel_in_wb(list_finish, 'dist', header_dist)


# coord_y_num_s - возвращает ближайшую УСПД по координатам из йоды в формате строки в сообщении
async def coord_uspd_db_coord_yoda_str(list_meters):

    query_uspd = func_psql.query_list_uspd()
    list_uspd = func_psql.sql_query_in_connect_db(query_uspd)

    list_meters_yoda = await yoda_func.requests_coord(list_meters)

    if len(list_meters_yoda) > 0:
        temp_list_meter = []
        for line_list_meters_yoda in list_meters_yoda:
            temp_list_meter.append(line_list_meters_yoda[0])
        list_finish = math_one_uspd_meter('str', list_meters_yoda, list_uspd)
        list_dif = dif_list(list_meters, temp_list_meter)
        if len(list_dif) > 0:
            for line_list_dif in list_dif:
                list_finish = list_finish + line_list_dif + ' - В ЙОДЕ нет такого ПУ или координат' + '\n'
        return list_finish
    else:
        list_error = ['В ЙОДЕ нет ни одного ПУ с таким(и) номером(ами) или координатами']
        return list_error


# coord_y_num_f - возвращает ближайшую УСПД по координатам из йоды в формате строки в сообщении
async def coord_uspd_db_coord_yoda_file(list_meters):

    query_uspd = func_psql.query_list_uspd()
    list_uspd = func_psql.sql_query_in_connect_db(query_uspd)

    list_meters_yoda = await yoda_func.requests_coord(list_meters)

    if len(list_meters_yoda) > 0:
        temp_list_meter = []
        for line_list_meters_yoda in list_meters_yoda:
            temp_list_meter.append(line_list_meters_yoda[0])
        list_finish = math_one_uspd_meter('file', list_meters_yoda, list_uspd)
        list_dif = dif_list(list_meters, temp_list_meter)
        if len(list_dif) > 0:
            for line_list_dif in list_dif:
                i = len(list_finish) + 1
                line_temp_error_meter = [i, line_list_dif, '', '', '', '', '', '', '', 'В ЙОДЕ нет такого ПУ или координат']
                list_finish.append(line_temp_error_meter)
        return excel_func.save_data_excel_in_wb(list_finish, 'dist', header_dist)
    else:
        list_error = ['В ЙОДЕ нет ни одного ПУ с таким(и) номером(ами) или координатами']
        return list_error


# входные координаты через файл
async def coord_uspd_db_file_coord_file(list_meters):

    query_uspd = func_psql.query_list_uspd()
    list_uspd = func_psql.sql_query_in_connect_db(query_uspd)

    list_finish = math_one_uspd_meter('file', list_meters, list_uspd)

    return excel_func.save_data_excel_in_wb(list_finish, 'dist', header_dist)

