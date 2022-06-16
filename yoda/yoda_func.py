from variables import basic, header_mac, username, password, url_auth, url_search, url_search_meter,\
    url_search_delivery, header_mac_str_y, header_short_mac_str_y
import requests
import json
from excel import excel_func
import datetime
from datetime import datetime
import re

basic_key = basic


# механизм авторизации с записью в файл
async def authorization_bas_key():

    headers = {'authorization': basic_key,
               'content-type': 'application/x-www-form-urlencoded'}

    url = url_auth

    data = {'grant_type': 'password', 'username': username, 'password': password}

    r = requests.post(url, headers=headers, data=data)

    text_requests = r.text
    load_key = json.loads(text_requests)

    text_requests = load_key['access_token']

    now_run = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    now_run = 'now = ' "\'" + str(now_run) + "\'" + "\n"
    access_token_w = 'access_token = ' + "\'" + 'Bearer ' + text_requests + "\'"

    f = open('variables_temp.py', 'w')
    f.write(now_run)
    f.write(access_token_w)
    f.close()

    authorization = 'Bearer ' + text_requests

    return authorization


# проверка ключа на валидность по времени
async def valid_yoda_key():

    authorization_var = ''
    token_time_var = ''

    # открыть файл с временнымыми переменными и получить bareer ключ
    f = open('variables_temp.py', 'r')

    i = 0
    for line_var in f:
        list_split_line = line_var
        list_split_line = re.split(r"[',.\n]\s*", list_split_line)
        if i == 0:
            token_time_var = list_split_line[1]
        if i == 1:
            authorization_var = list_split_line[1]
        i += 1

    f.close()

    now_time = datetime.now()
    token_time = datetime.strptime(token_time_var, '%Y-%m-%d %H:%M:%S')

    delta = now_time - token_time

    seconds = delta.total_seconds()

    if seconds > 43200:
        authorization = await authorization_bas_key()
    else:
        authorization = authorization_var

    return authorization


# создание запроса и отправка запроса в йоду
async def create_requests(list_meter, search, view, url_var):

    authorization = await valid_yoda_key()

    # формаирование json запроса
    data_json = {"filter": {"conditions": [{"property": search, "value": list_meter, "operator": "in"}]},
                 "view": view}

    url = url_var  # url поиска из файла с переменными
    headers = {'authorization': authorization,
               'content-type': 'application/json'}

    r = requests.post(url, headers=headers, json=data_json)  # запрос к апи йоды

    if r.status_code != 200:
        print(r)
        authorization = await authorization_bas_key()
        headers = {'authorization': authorization,
                   'content-type': 'application/json'}
        r = requests.post(url, headers=headers, json=data_json)  # запрос к апи йоды

    text_requests = r.text
    load_list = json.loads(text_requests)

    return load_list


# запрос координат в йоде DeliveryPoint
async def requests_coord(list_meter):

    search = 'number'
    view = 'mobile-stolbi'

    result_request_meter = await create_requests(list_meter, search, view, url_search_meter)

    list_meter_id = []
    for line_result_request_meter in result_request_meter:
        id_meter = line_result_request_meter['id']
        list_meter_id.append(id_meter)

    search = 'meter'
    view = 'edit'
    result_request_delivery = await create_requests(list_meter_id, search, view, url_search_delivery)

    number_meter = ''
    list_meter_delivery = []
    for line_result_request_delivery in result_request_delivery:
        id_meter_delv = line_result_request_delivery['meter']['id']
        latitude = line_result_request_delivery['latitude']
        longitude = line_result_request_delivery['longitude']
        for line_result_request_meter in result_request_meter:
            if line_result_request_meter['id'] == id_meter_delv:
                number_meter = line_result_request_meter['number']

        list_temp_delv = [number_meter, latitude, longitude]
        list_meter_delivery.append(list_temp_delv)

    return list_meter_delivery


async def id_meter_meter_type(list_meter, search, view):

    load_list = []
    authorization_var = ''
    token_time_var = ''

    # открыть файл с временнымыми переменными и получить bareer ключ
    f = open('variables_temp.py', 'r')

    i = 0
    for line_var in f:
        list_split_line = line_var
        list_split_line = re.split(r"[',.\n]\s*", list_split_line)
        if i == 0:
            token_time_var = list_split_line[1]
        if i == 1:
            authorization_var = list_split_line[1]
        i += 1

    f.close()

    # проверка ключа на валидность по времени создания
    now_time = datetime.now()
    token_time = datetime.strptime(token_time_var, '%Y-%m-%d %H:%M:%S')

    delta = now_time - token_time

    seconds = delta.total_seconds()

    if seconds > 43200:
        authorization = await authorization_bas_key()
    else:
        authorization = authorization_var

    list_id = []

    if len(list_meter) > 1000:

        i_start_range = 0
        j_end_range = 1000
        while j_end_range <= len(list_meter):

            list_meter_temp = list_meter[i_start_range:j_end_range]

            # формаирование json запроса
            data_json = {"filter": {"conditions": [{"property": search, "value": list_meter_temp, "operator": "in"}]}, "view": view}

            url = url_search  # url поиска из файла с переменными
            headers = {'authorization': authorization,
                       'content-type': 'application/json'}
            r = requests.post(url, headers=headers, json=data_json)  # запрос к апи йоды

            if r.status_code != 200:
                print(r)
                authorization = await authorization_bas_key()
                headers = {'authorization': authorization,
                           'content-type': 'application/json'}
                r = requests.post(url, headers=headers, json=data_json)  # запрос к апи йоды

            text_requests = r.text
            load_list_temp = json.loads(text_requests)

            load_list.extend(list(load_list_temp))

            i_start_range = j_end_range

            if j_end_range + 1000 >= len(list_meter):
                a = len(list_meter) - j_end_range
                if len(list_meter) - j_end_range > 1:
                    j_end_range = j_end_range + (len(list_meter) - j_end_range)
                else:
                    break
            else:
                j_end_range += 1000
    else:

        data_json = {"filter": {"conditions": [{"property": search, "value": list_meter, "operator": "in"}]},
                     "view": view}

        url = url_search  # url поиска из файла с переменными
        headers = {'authorization': authorization,
                   'content-type': 'application/json'}
        r = requests.post(url, headers=headers, json=data_json)  # запрос к апи йоды

        if r.status_code != 200:
            print(r)
            authorization = await authorization_bas_key()
            headers = {'authorization': authorization,
                       'content-type': 'application/json'}
            r = requests.post(url, headers=headers, json=data_json)  # запрос к апи йоды

        text_requests = r.text
        load_list_temp = json.loads(text_requests)

        load_list.extend(list(load_list_temp))

    i = 0
    for list_line in load_list:
        list_id.append([])
        if 'number' in list_line:
            list_id[i].append(list_line['number'])
        else:
            list_id[i].append('No number')
        if 'mac' in list_line:
            list_id[i].append(list_line['mac'])
        else:
            list_id[i].append('No mac')
        list_id[i].append(list_line['id'])
        if list_line['meterType']['_instanceName'] != None:
            list_id[i].append(list_line['meterType']['_instanceName'])
        else:
            list_id[i].append('Нет расширенного типа - '+list_line['type'])
        i += 1

    if search == 'number':
        temp_list = []
        for line_temp in list_id:
            temp_list.append(line_temp[0])

    if search == 'mac':
        temp_list = []
        for line_temp in list_id:
            temp_list.append(line_temp[1])

    i = 0
    final_list = []
    for line_list_meter in list_meter:
        try:
            index_meter = temp_list.index(line_list_meter)
            final_list.append(list_id[index_meter])


        except:
            if search == 'number':
                final_list.append([line_list_meter, 'ПУ с таким MAC нет в базе'])
            if search == 'mac':
                final_list.append(['ПУ с таким MAC нет в базе', line_list_meter])

    mas = excel_func.save_data_excel_in_wb(final_list, 'yoda', header_mac)

    return mas


async def id_meter_meter_type_src(list_meter, search, view):

    f = open('variables_temp.py', 'r')

    i = 0
    for line_var in f:
        list_split_line = line_var
        list_split_line = re.split(r"[',.\n]\s*", list_split_line)
        if i == 0:
            token_time_var = list_split_line[1]
        if i == 1:
            authorization_var = list_split_line[1]
        i += 1

    f.close()

    now_time = datetime.now()
    token_time = datetime.strptime(token_time_var, '%Y-%m-%d %H:%M:%S')

    delta = now_time - token_time

    seconds = delta.total_seconds()

    if seconds > 43200:
        authorization = await authorization_bas_key()
    else:
        authorization = authorization_var

    list_id = []

    data_json = {"filter": {"conditions": [{"property": search, "value": list_meter, "operator": "in"}]}, "view": view}

    url = url_search
    headers = {'authorization': authorization,
               'content-type': 'application/json'}
    r = requests.post(url, headers=headers, json=data_json)

    if r.status_code != 200:
        print(r)
        authorization = await authorization_bas_key()
        headers = {'authorization': authorization,
                   'content-type': 'application/json'}
        r = requests.post(url, headers=headers, json=data_json)  # запрос к апи йоды

    text_requests = r.text
    load_list = json.loads(text_requests)

    i = 0
    for list_line in load_list:
        list_id.append([])
        if 'number' in list_line:
            list_id[i].append(list_line['number'])
        else:
            list_id[i].append('No number')
        if 'mac' in list_line:
            list_id[i].append(list_line['mac'])
        else:
            list_id[i].append('No mac')
        # list_id[i].append(list_line['id'])
        if list_line['meterType']['_instanceName'] != None:
            list_id[i].append(list_line['meterType']['_instanceName'])
        else:
            list_id[i].append('Нет расширенного типа - ' + list_line['type'])
        i += 1

    if search == 'number':
        temp_list = []
        for line_temp in list_id:
            temp_list.append(line_temp[0])

    if search == 'mac':
        temp_list = []
        for line_temp in list_id:
            temp_list.append(line_temp[1])

    i = 0
    final_list = []
    for line_list_meter in list_meter:
        try:
            index_meter = temp_list.index(line_list_meter)
            final_list.append(list_id[index_meter])
        except:
            if search == 'number':
                final_list.append([line_list_meter, 'ПУ с таким MAC нет в базе'])
            if search == 'mac':
                final_list.append(['ПУ с таким MAC нет в базе', line_list_meter])

    # mas = excel_func.save_data_excel_in_wb(final_list, 'yoda', header_mac)

    StrB = header_mac_str_y
    count_line_str = 1
    for line_final_output in final_list:
        StrA = str(count_line_str) + " " + " ".join(line_final_output) + '\n'
        StrB = StrB + StrA
        count_line_str += 1

    return StrB


async def id_meter_short_src(list_meter, search, view):

    f = open('variables_temp.py', 'r')

    i = 0
    for line_var in f:
        list_split_line = line_var
        list_split_line = re.split(r"[',.\n]\s*", list_split_line)
        if i == 0:
            token_time_var = list_split_line[1]
        if i == 1:
            authorization_var = list_split_line[1]
        i += 1

    f.close()

    now_time = datetime.now()
    token_time = datetime.strptime(token_time_var, '%Y-%m-%d %H:%M:%S')

    delta = now_time - token_time

    seconds = delta.total_seconds()

    if seconds > 43200:
        authorization = await authorization_bas_key()
    else:
        authorization = authorization_var

    list_id = []

    data_json = {"filter": {"conditions": [{"property": search, "value": list_meter, "operator": "in"}]}, "view": view}

    url = url_search
    headers = {'authorization': authorization,
               'content-type': 'application/json'}
    r = requests.post(url, headers=headers, json=data_json)

    if r.status_code != 200:
        print(r)
        authorization = await authorization_bas_key()
        headers = {'authorization': authorization,
                   'content-type': 'application/json'}
        r = requests.post(url, headers=headers, json=data_json)  # запрос к апи йоды

    # print(r)
    text_requests = r.text
    print(text_requests)
    load_list = json.loads(text_requests)
    print(load_list)

    i = 0
    for list_line in load_list:
        list_id.append([])
        if 'number' in list_line:
            list_id[i].append(list_line['number'])
        else:
            list_id[i].append('No number')
        if 'mac' in list_line:
            list_id[i].append(list_line['mac'])
        else:
            list_id[i].append('No mac')
        # list_id[i].append(list_line['id'])
        # if list_line['meterType']['_instanceName'] != None:
        #     list_id[i].append(list_line['meterType']['_instanceName'])
        # else:
        #     list_id[i].append('Нет расширенного типа - ' + list_line['type'])
        i += 1

    if search == 'number':
        temp_list = []
        for line_temp in list_id:
            temp_list.append(line_temp[0])

    if search == 'mac':
        temp_list = []
        for line_temp in list_id:
            temp_list.append(line_temp[1])

    i = 0
    final_list = []
    for line_list_meter in list_meter:
        try:
            index_meter = temp_list.index(line_list_meter)
            final_list.append(list_id[index_meter])
        except:
            if search == 'number':
                final_list.append([line_list_meter, 'ПУ с таким MAC нет в базе'])
            if search == 'mac':
                final_list.append(['ПУ с таким MAC нет в базе', line_list_meter])

    # mas = excel_func.save_data_excel_in_wb(final_list, 'yoda', header_mac)

    StrB = ''

    for line_final_output in final_list:
        if search == 'number':
            StrA = str(line_final_output[1]) + '\n'
            StrB = StrB + StrA
        if search == 'mac':
            StrA = str(line_final_output[0]) + '\n'
            StrB = StrB + StrA

    return StrB
