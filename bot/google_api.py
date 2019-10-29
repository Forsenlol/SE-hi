import time
import gspread
import os
import logging
import json
from config import MODE, GOOGLE_API_TOKEN, TABLE_NAME
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

USER_NAME_COL_NUM = 2
TIME_COL_NUM = 1

# Функция для поиска индекса последнего вхождения значения val в список


def rindex(lst, val):
    try:
        i = lst[::-1].index(val, 0, len(lst))
        return i
    except ValueError:
        return -1


def result(row):
    komb = [row[2:7], ['3', '899076', '441', '371', '15625']]
    teorver = [row[7:12], ['11 216 28', 'да', '0.0116', '0.52', '6']]
    matanaliz = [row[12:17], ['0.0025', '-30.069', '-0.1489', '116', '5']]
    lineyka = [row[17:22], ['2', '0', '6', '3; 0', '(0.5; 1), (-1; 1)']]
    algos = [row[22:27], ['f3,f2,f4,f1', 'B', 'O(logn)', 'O(nlogn)', 'Нет']]
    general_issues = [row[27:30], ['меньше 4 часов ', 'Нет', 'Нет', 'Нет']]
    otvety = [[], []]
    tmp = [i for i, j in zip(komb[0], komb[1]) if i == j]
    otvety[0].append(len(tmp))
    otvety[0].append('Комбинаторика')
    tmp = [i for i, j in zip(teorver[0], teorver[1]) if i == j]
    otvety[1].append(len(tmp))
    otvety[1].append('Теорвер')
    tmp = [i for i, j in zip(matanaliz[0], matanaliz[1]) if i == j]
    otvety[2].append(len(tmp))
    otvety[2].append('Матанализ')
    tmp = [i for i, j in zip(lineyka[0], lineyka[1]) if i == j]
    otvety[3].append(len(tmp))
    otvety[3].append('Линейная Алгебра')
    tmp = [i for i, j in zip(algos[0], algos[1]) if i == j]
    otvety[4].append(len(tmp))
    otvety[4].append('Алгоритмы')
    res = []
    for i in range(0, 4):
        if general_issues[0][i] != general_issues[1][i]:
            res.append(1)
        else:
            res.append(0)
    return otvety, res


def get_sheet():
    if not hasattr(get_sheet, 'sheet'):
        scope = ["https://spreadsheets.google.com/feeds",
                 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file",
                 "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            json.loads(GOOGLE_API_TOKEN), scope)
        logger.info("Getting credentials")

        client = gspread.authorize(creds)
        setattr(get_sheet, 'sheet', client.open(TABLE_NAME).sheet1)

    return get_sheet.sheet


def get_api(telegram_login, date_telegram_login):
    sheet = get_sheet()

    # data = sheet.get_all_records()

    user_col = sheet.col_values(USER_NAME_COL_NUM)
    user_responses = len(user_col) - rindex(user_col, telegram_login)

    time_col = sheet.col_values(TIME_COL_NUM)
    if len(time_col) == 1:
        date_time_sheet = datetime.fromtimestamp(time.mktime(time.gmtime(0)))
    else:
        date_time_sheet = datetime.\
            strptime(sheet.col_values(1)[user_responses], '%d.%m.%Y %H:%M:%S')

    logger.info(
        f"Waiting for {telegram_login} form submission at {date_telegram_login}")
    if date_time_sheet > date_telegram_login:
        logger.info("Got it")
        return sheet.row_values(user_responses)

    stop_time = time.time()
    TIME_FOR_SUMBISSION_S = 30
    while rindex(user_col, telegram_login) == -1:
        time.sleep(5)
        if time.time() > stop_time + TIME_FOR_SUMBISSION_S:
            break
        user_col = sheet.col_values(USER_NAME_COL_NUM)
        user_responses = len(user_col) - rindex(user_col, telegram_login)

    logger.info(
        f"Got it for {telegram_login} form submission at {date_telegram_login}")
    return sheet.row_values(user_responses)


if __name__ == "__main__":
    get_api('bot6')
