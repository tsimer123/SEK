from aiogram import types, Dispatcher
from create_bot import dp, bot
from yoda import yoda_func
from zabbix import zabbix_func
import re
import urllib.request
from variables import TOKEN
import requests, json
import datetime
from excel import excel_func
from cli import func_cli
from sql import func_sql
from coordinates_math import func_coordinat


async def command_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Добро пожаловать')
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему:\nhttps://t.me/PNR_SEK_bot')


async def command_help(message: types.Message):
    id_user = message.from_user.id
    full_name = message.from_user.full_name
    tg_name = message.from_user.mention
    print(str(datetime.datetime.now()) + ' ' + tg_name + ' ' + str(id_user) + ' ' + full_name + ' ' + str(message.text))

    list_help = []
    str_help = ''

    with open("help.txt", 'r', encoding='utf8') as f_help:
        list_help = f_help.readlines()
    for line_f in list_help:
        str_help += line_f
    await message.reply(str_help, parse_mode="MarkdownV2")


async def yoda_mac(message: types.Message):
    id_user = message.from_user.id
    full_name = message.from_user.full_name
    tg_name = message.from_user.mention
    print(str(datetime.datetime.now()) + ' ' + tg_name + ' ' + str(id_user) + ' ' + full_name + ' ' + str(message.text))
    number = message.text[5:]
    number = re.split(r"[-;,.\s]\s*", number)
    number_filter = list(filter(None, number))
    search = 'number'  # number, mac
    view = 'mobile-stolbi'  # _minimal, mobile-stolbi
    file_mane = await yoda_func.id_meter_meter_type(number_filter, search, view)
    await message.reply_document(open(file_mane, 'rb'))


async def yoda_mac_src(message: types.Message):
    id_user = message.from_user.id
    full_name = message.from_user.full_name
    tg_name = message.from_user.mention
    print(str(datetime.datetime.now()) + ' ' + tg_name + ' ' + str(id_user) + ' ' + full_name + ' ' + str(message.text))
    number = message.text[7:]
    number = re.split(r"[-;,.\s]\s*", number)
    number_filter = list(filter(None, number))
    search = 'number'  # number, mac
    view = 'mobile-stolbi'  # _minimal, mobile-stolbi
    # file_mane = yoda_func.id_meter_meter_type(number_filter, search, view)
    output_source = await yoda_func.id_meter_meter_type_src(number_filter, search, view)
    await message.reply(output_source)


async def yoda_mac_short_src(message: types.Message):
    id_user = message.from_user.id
    full_name = message.from_user.full_name
    tg_name = message.from_user.mention
    print(str(datetime.datetime.now()) + ' ' + str(id_user) + ' ' + full_name + ' ' + str(message.text))
    number = message.text[6:]
    number = re.split(r"[-;,.\s]\s*", number)
    number_filter = list(filter(None, number))
    search = 'number'  # number, mac
    view = 'mobile-stolbi'  # _minimal, mobile-stolbi
    # file_mane = yoda_func.id_meter_meter_type(number_filter, search, view)
    output_source = await yoda_func.id_meter_short_src(number_filter, search, view)
    await message.reply(output_source)


async def yoda_num(message: types.Message):
    id_user = message.from_user.id
    full_name = message.from_user.full_name
    tg_name = message.from_user.mention
    print(str(datetime.datetime.now()) + ' ' + tg_name + ' ' + str(id_user) + ' ' + full_name + ' ' + str(message.text))
    number = message.text[5:]
    number = re.split(r"[-;,.\s]\s*", number)
    number_filter = list(filter(None, number))
    search = 'mac'  # number, mac
    view = 'mobile-stolbi'  # _minimal, mobile-stolbi
    # file_mane = yoda_func.id_meter_meter_type(number_filter, search, view)
    await message.reply_document(open(await yoda_func.id_meter_meter_type(number_filter, search, view), 'rb'))


async def yoda_num_src(message: types.Message):
    id_user = message.from_user.id
    full_name = message.from_user.full_name
    tg_name = message.from_user.mention
    print(str(datetime.datetime.now()) + ' ' + tg_name + ' ' + str(id_user) + ' ' + full_name + ' ' + str(message.text))
    number = message.text[7:]
    number = re.split(r"[-;,.\s]\s*", number)
    number_filter = list(filter(None, number))
    search = 'mac'  # number, mac
    view = 'mobile-stolbi'  # _minimal, mobile-stolbi
    # output_source = yoda_func.id_meter_meter_type_src(number_filter, search, view)
    await message.reply(await yoda_func.id_meter_meter_type_src(number_filter, search, view))


async def yoda_num_short_src(message: types.Message):
    id_user = message.from_user.id
    full_name = message.from_user.full_name
    tg_name = message.from_user.mention
    print(str(datetime.datetime.now()) + ' ' + tg_name + ' ' + str(id_user) + ' ' + full_name + ' ' + str(message.text))
    number = message.text[6:]
    number = re.split(r"[-;,.\s]\s*", number)
    number_filter = list(filter(None, number))
    search = 'mac'  # number, mac
    view = 'mobile-stolbi'  # _minimal, mobile-stolbi
    # output_source = yoda_func.id_meter_short_src(number_filter, search, view)
    await message.reply(await yoda_func.id_meter_short_src(number_filter, search, view))


async def document_send(message: types.Message):
    # await message.reply_document(open('bot_iogram\\10.144.57.26.csv', 'rb'))
    await message.reply_document(open('file\\test\\Березники - не найденные ПУ.xlsx', 'rb'))
    # await bot.send_message(message.from_user.id, 'ул. Колбасная 15')


async def zabbix_ip(message: types.Message):
    id_user = message.from_user.id
    full_name = message.from_user.full_name
    tg_name = message.from_user.mention
    print(str(datetime.datetime.now()) + ' ' + tg_name + ' ' + str(id_user) + ' ' + full_name + ' ' + str(message.text))
    ip = message.text[3:]
    ip = re.split(r"[-;,\s]\s*", ip)
    ip_filter = list(filter(None, ip))
    first_element = ip_filter[0]
    if first_element.isdigit():
        query_limit = str(int(ip_filter[0])*len(ip_filter))
        ip_filter.pop(0)
    else:
        query_limit = len(ip_filter)*20
    file_mane = zabbix_func.get_avg(ip_filter, query_limit)
    await message.reply_document(open(file_mane, 'rb'))


async def zabbix_ip_src(message: types.Message):
    id_user = message.from_user.id
    full_name = message.from_user.full_name
    tg_name = message.from_user.mention
    print(str(datetime.datetime.now()) + ' ' + tg_name + ' ' + str(id_user) + ' ' + full_name + ' ' + str(message.text))
    ip = message.text[5:]
    ip = re.split(r"[-;,\s]\s*", ip)
    ip_filter = list(filter(None, ip))
    first_element = ip_filter[0]
    if first_element.isdigit():
        query_limit = str(int(ip_filter[0])*len(ip_filter))
        ip_filter.pop(0)
    else:
        query_limit = len(ip_filter)*20
    output_source = zabbix_func.get_avg_src(ip_filter, query_limit)
    await message.reply(output_source)


async def download_file(message):
    id_user = message.from_user.id
    full_name = message.from_user.full_name
    tg_name = message.from_user.mention
    print(str(datetime.datetime.now()) + ' ' + tg_name + ' ' + str(id_user) + ' ' + full_name + ' ' + str(message.text))
    id = message.document.file_id
    res = requests.get('https://api.telegram.org/bot{}/getFile?file_id={}'.format(TOKEN, id))
    b = json.loads(res.text)
    file_id = b['result']['file_path']
    name = message.document.file_name
    print(name)
    now = datetime.datetime.now()
    now = str(now).replace(':', '_')
    dir_file = f'./file/input/{now}-{name}'
    urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{TOKEN}/{file_id}', dir_file)
    name_file = name.split('_')
    number_filter = excel_func.open_excel(dir_file)
    number_filter_in_func = []
    for meter_line in number_filter:
        number_filter_in_func.append(str(meter_line[0]))
    if name_file[0] == 'num':
        search = 'mac'  # number, mac
        view = 'mobile-stolbi'  # _minimal, mobile-stolbi
        file_mane = await yoda_func.id_meter_meter_type(number_filter_in_func, search, view)
        await message.reply_document(open(file_mane, 'rb'))
    elif name_file[0] == 'mac':
        search = 'number'  # number, mac
        view = 'mobile-stolbi'  # _minimal, mobile-stolbi
        file_mane = await yoda_func.id_meter_meter_type(number_filter_in_func, search, view)
        await message.reply_document(open(file_mane, 'rb'))
    elif name_file[0] == 'coord':
        result = await func_coordinat.coord_uspd_db_file_coord_file(number_filter)
        if not isinstance(result, str):
            await message.reply_document(open(result, 'rb'))
        else:
            await message.reply(result)
    else:
        await message.reply('Файл с некорректным названием')


async def change_net_open(message: types.Message):

    id_user = message.from_user.id
    full_name = message.from_user.full_name
    tg_name = message.from_user.mention
    print(str(datetime.datetime.now()) + ' ' + tg_name + ' ' + str(id_user) + ' ' + full_name + ' ' + str(message.text))
    status_change = []
    list_status_change = []
    ip = message.text[9:]
    ip = re.split(r"[-;,\s]\s*", ip)
    ip_filter = list(filter(None, ip))
    for line in ip_filter:
        status_change = await func_cli.change_condition_net(line, id_user, get_change='open')
        list_status_change.append(status_change)
    StrB = ''
    for line in list_status_change:
        StrA = str(line[0]) + ' ' + str(line[1]) + '\n'
        StrB = StrB + StrA
    await message.reply(StrB)


async def change_net_close(message: types.Message):
    id_user = message.from_user.id
    full_name = message.from_user.full_name
    tg_name = message.from_user.mention
    print(str(datetime.datetime.now()) + ' ' + tg_name + ' ' + str(id_user) + ' ' + full_name + ' ' + str(message.text))
    status_change = []
    list_status_change = []
    ip = message.text[10:]
    ip = re.split(r"[-;,\s]\s*", ip)
    ip_filter = list(filter(None, ip))
    for line in ip_filter:
        status_change = await func_cli.change_condition_net(line, id_user, get_change='close')
        list_status_change.append(status_change)
    StrB = ''
    for line in list_status_change:
        StrA = str(line[0]) + ' ' + str(line[1]) + '\n'
        StrB = StrB + StrA
    await message.reply(StrB)


async def netinfo_in_sql_db(message: types.Message):
    id_user = message.from_user.id
    full_name = message.from_user.full_name
    tg_name = message.from_user.mention
    print(str(datetime.datetime.now()) + ' ' + tg_name + ' ' + str(id_user) + ' ' + full_name + ' ' + str(message.text))
    list_netinfo = []
    # list_status_change = []
    ip = message.text[6:]
    ip = re.split(r"[-;,\s]\s*", ip)
    ip_filter = list(filter(None, ip))
    for line in ip_filter:
        sqlite_query_host_id = func_sql.select_host_netinfo_all(line)
        netinfo_host = func_sql.sql_query_select(sqlite_query_host_id)
        if len(netinfo_host) > 0:
            list_netinfo.append(netinfo_host[0])
        else:
            list_netinfo.append([line, 'Такого IP нет в БД'])
    StrC = ''
    count_output = 1
    for line in list_netinfo:
        StrB = str(count_output) + ' '
        for element in line:
            if element is not None:
                StrA = str(element) + ' '
                StrB = StrB + StrA
        StrC = StrC + StrB + '\n'
        count_output += 1
    await message.reply(StrC)


async def coordinates_test(message: types.Message):
    list_meter_values = []
    id_user = message.from_user.id
    full_name = message.from_user.full_name
    tg_name = message.from_user.mention
    print(str(datetime.datetime.now()) + ' ' + tg_name + ' ' + str(id_user) + ' ' + full_name + ' ' + str(message.text))
    meter_values = message.text[8:]
    meter_values = re.split(r"[-;,\s]\s*", meter_values)
    meter_values_filter = list(filter(None, meter_values))
    list_meter_values.append(meter_values_filter)
    if len(meter_values_filter) == 3:
        await message.reply_document(open(await func_coordinat.coord_uspd_db_meter_user(list_meter_values), 'rb'))
    else:
        await message.reply('Не верный формат записи команды ' + str(meter_values_filter))


# coorddb_nums вернет все УСПД в радиусе 10км для ПУ из БД
async def coordinates_number_meters(message: types.Message):
    id_user = message.from_user.id
    full_name = message.from_user.full_name
    tg_name = message.from_user.mention
    print(str(datetime.datetime.now()) + ' ' + tg_name + ' ' + str(id_user) + ' ' + full_name + ' ' + str(message.text))
    meters = message.text[13:]
    meters = re.split(r"[;,\s]\s*", meters)
    meters_filter = list(filter(None, meters))

    if len(meters_filter) > 0:
        result = await func_coordinat.coord_uspd_db_num_meters_user(meters_filter)
        if not isinstance(result, list):
            await message.reply_document(open(result, 'rb'))
        else:
            await message.reply(result[0])
    else:
        await message.reply('Данные для обработки не введены')


# coordBD_num_f - возвращает ближайшую УСПД для списка ПУ в формате файла
async def coord_one_uspd_db_meter_user_out_file(message: types.Message):
    id_user = message.from_user.id
    full_name = message.from_user.full_name
    tg_name = message.from_user.mention
    print(str(datetime.datetime.now()) + ' ' + tg_name + ' ' + str(id_user) + ' ' + full_name + ' ' + str(message.text))
    meters = message.text[14:]
    meters = re.split(r"[;,\s]\s*", meters)
    meters_filter = list(filter(None, meters))

    if len(meters_filter) > 0:
        result = await func_coordinat.coord_uspd_db_one_meter_user_file(meters_filter)
        if not isinstance(result, list):
            await message.reply_document(open(result, 'rb'))
        else:
            await message.reply(result[0])
    else:
        await message.reply('Данные для обработки не введены')


# coordBD_num_s - возвращает ближайшую УСПД для списка ПУ в формате строке в сообщении
async def coord_one_uspd_db_meter_user_out_str(message: types.Message):
    id_user = message.from_user.id
    full_name = message.from_user.full_name
    tg_name = message.from_user.mention
    print(str(datetime.datetime.now()) + ' ' + tg_name + ' ' + str(id_user) + ' ' + full_name + ' ' + str(message.text))
    meters = message.text[14:]
    meters = re.split(r"[;,\s]\s*", meters)
    meters_filter = list(filter(None, meters))

    if len(meters_filter) > 0:
        result = await func_coordinat.coord_uspd_db_one_meter_user_str(meters_filter)
        if isinstance(result, str):
            await message.reply(result)
        else:
            await message.reply(result[0])
    else:
        await message.reply('Данные для обработки не введены')


# coord_ll_s - возвращает ближайшую УСПД по координатам пользователя в формате строки в сообщении
async def coord_one_uspd_db_coord_user_out_str(message: types.Message):
    id_user = message.from_user.id
    full_name = message.from_user.full_name
    tg_name = message.from_user.mention
    print(str(datetime.datetime.now()) + ' ' + tg_name + ' ' + str(id_user) + ' ' + full_name + ' ' + str(message.text))
    coords = message.text[11:]
    coords = re.split(r"[;,\s]\s*", coords)
    coords_filter = list(filter(None, coords))

    if len(coords_filter) > 0:
        if len(coords_filter) == 2:
            result = await func_coordinat.coord_uspd_db_coord_user_str(coords_filter)
            if isinstance(result, str):
                await message.reply(result)
            else:
                await message.reply(result[0])
        else:
            await message.reply('Не верный формат записи команды (55.755819 37.617644)')
    else:
        await message.reply('Данные для обработки не введены')


# coord_ll_f - возвращает ближайшую УСПД по координатам пользователя в формате файла
async def coord_one_uspd_db_coord_user_out_file(message: types.Message):
    id_user = message.from_user.id
    full_name = message.from_user.full_name
    tg_name = message.from_user.mention
    print(str(datetime.datetime.now()) + ' ' + tg_name + ' ' + str(id_user) + ' ' + full_name + ' ' + str(message.text))
    coords = message.text[11:]
    coords = re.split(r"[;,\s]\s*", coords)
    coords_filter = list(filter(None, coords))

    if len(coords_filter) > 0:
        if len(coords_filter) == 2:
            result = await func_coordinat.coord_uspd_db_coord_user_file(coords_filter)
            if not isinstance(result, list):
                await message.reply_document(open(result, 'rb'))
            else:
                await message.reply(result[0])
        else:
            await message.reply('Не верный формат записи команды (55.755819 37.617644)')
    else:
        await message.reply('Данные для обработки не введены')


# coord_y_num_s - возвращает ближайшую УСПД по координатам из йоды в формате строки в сообщении
async def coord_uspd_db_meter_yoda_out_str(message: types.Message):
    id_user = message.from_user.id
    full_name = message.from_user.full_name
    tg_name = message.from_user.mention
    print(str(datetime.datetime.now()) + ' ' + tg_name + ' ' + str(id_user) + ' ' + full_name + ' ' + str(message.text))
    meters = message.text[14:]
    meters = re.split(r"[;,\s]\s*", meters)
    meters_filter = list(filter(None, meters))

    if len(meters_filter) > 0:
        result = await func_coordinat.coord_uspd_db_coord_yoda_str(meters_filter)
        if isinstance(result, str):
            await message.reply(result)
        else:
            await message.reply(result[0])
    else:
        await message.reply('Данные для обработки не введены')


# coord_y_num_f - возвращает ближайшую УСПД по координатам из йоды в формате файла
async def coord_uspd_db_meter_yoda_out_file(message: types.Message):
    id_user = message.from_user.id
    full_name = message.from_user.full_name
    tg_name = message.from_user.mention
    print(str(datetime.datetime.now()) + ' ' + tg_name + ' ' + str(id_user) + ' ' + full_name + ' ' + str(message.text))
    meters = message.text[14:]
    meters = re.split(r"[;,\s]\s*", meters)
    meters_filter = list(filter(None, meters))

    if len(meters_filter) > 0:
        result = await func_coordinat.coord_uspd_db_coord_yoda_file(meters_filter)
        if not isinstance(result, list):
            await message.reply_document(open(result, 'rb'))
        else:
            await message.reply(result[0])
    else:
        await message.reply('Данные для обработки не введены')


def register_handler_client(db: Dispatcher):
    # dp.register_message_handler(unknown_message, content_types=['ANY'])
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_help, commands=['help'])
    dp.register_message_handler(yoda_mac, commands=['mac'])
    dp.register_message_handler(yoda_mac_src, commands=['mac_sa'])
    dp.register_message_handler(yoda_mac_short_src, commands=['mac_s'])
    dp.register_message_handler(yoda_num, commands=['num'])
    dp.register_message_handler(yoda_num_src, commands=['num_sa'])
    dp.register_message_handler(yoda_num_short_src, commands=['num_s'])
    dp.register_message_handler(zabbix_ip, commands=['ip'])
    dp.register_message_handler(zabbix_ip_src, commands=['ip_s'])
    dp.register_message_handler(document_send, commands=['send'])
    dp.register_message_handler(download_file, content_types=['document'])
    dp.register_message_handler(change_net_open, commands=['cli_open'])
    dp.register_message_handler(change_net_close, commands=['cli_close'])
    dp.register_message_handler(netinfo_in_sql_db, commands=['ni_db'])
    dp.register_message_handler(coordinates_test, commands=['coord_t'])
    dp.register_message_handler(coordinates_number_meters, commands=['coorddb_nums'])
    dp.register_message_handler(coord_one_uspd_db_meter_user_out_file, commands=['coorddb_num_f'])
    dp.register_message_handler(coord_one_uspd_db_meter_user_out_str, commands=['coorddb_num_s'])
    dp.register_message_handler(coord_one_uspd_db_coord_user_out_str, commands=['coord_ll_s'])
    dp.register_message_handler(coord_one_uspd_db_coord_user_out_file, commands=['coord_ll_f'])
    dp.register_message_handler(coord_uspd_db_meter_yoda_out_str, commands=['coord_y_num_s'])
    dp.register_message_handler(coord_uspd_db_meter_yoda_out_file, commands=['coord_y_num_f'])


