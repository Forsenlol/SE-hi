# from face_rec import face_rec
from graphs import graphs
from config import MODE, GOOGLE_API_TOKEN, TABLE_NAME
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import time
import gspread
import os
import logging
import json

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


def result_return(d, otvety, otvety_name, poshalky):
    comment = []
    comment_poshalky = []
    for i in range(0, len(otvety)):
        if otvety[i] < 4:
            comment.extend(d[otvety_name[i]])
    if poshalky[0] == 1:
        comment_poshalky.append(d['time'])
    if poshalky[1] == 1:
        comment_poshalky.append(d['Job'])
    if poshalky[2] == 1:
        comment_poshalky.append(d['Deadlines'])
    if poshalky[3] == 1:
        comment_poshalky.append(d['Лапки'])
    return comment_poshalky, comment


def dictionary():
    d = {'Комбинаторика': ['Для успешной сдачи вступительных испытаний советуем вам ознакомиться с данными курсами:', 'https://stepik.org/course/91/syllabus', 'https://stepik.org/course/125/promo'],
         'Теорвер': ['Для успешной сдачи вступительных испытаний советуем вам ознакомиться с данными курсами:', 'https://stepik.org/course/3089/syllabus', 'https://www.coursera.org/browse/data-science/probability-and-statistics'],
         'Матанализ': ['Для успешной сдачи вступительных испытаний советуем вам ознакомиться с данными курсами:', 'https://stepik.org/course/716/syllabus', 'https://stepik.org/course/711/promo'],
         'Линейная Алгебра': ['Для успешной сдачи вступительных испытаний советуем вам ознакомиться с данными курсами:', 'https://www.coursera.org/learn/algebra-lineynaya', 'https://stepik.org/course/2461/promo'],
         'Алгоритмы': ['Для успешной сдачи вступительных испытаний советуем вам ознакомиться с данными курсами:', 'https://stepik.org/course/217/promo', 'https://www.coursera.org/browse/computer-science/algorithms'],
         'time': 'Будьте готовы к тому, что из-за высокой интенсивности обучения, Вам придется спать намного меньше :)',
         'Job': 'На нашем направлении слишком активная студенческая жизнь в плане учебы, поэтому Вам навряд ли удастся совмещать обучение с работой.',
         'Deadlines': 'Будьте готовы к тому, что Вы столкнетесь с большими проблемами, так как каждый день Вам будет необходимо делать новую задачку, и если они вдруг накопятся....',
         'Лапки': 'Домашние работы на нашем направлении сложнее в 10 раз.'}
    return d


def result(row):
    komb = [row[2:7], ['3', '899076', '441', '371', '15625']]
    teorver = [row[7:12], ['11 216 28', 'да', '0.0116', '0.52', '6']]
    matanaliz = [row[12:17], ['0.0025', '-30.069', '-0.1489', '116', '5']]
    lineyka = [row[17:22], ['2', '0', '6', '3; 0', '(0.5; 1), (-1; 1)']]
    algos = [row[22:27], ['f3,f2,f4,f1', 'B', 'O(logn)', 'O(nlogn)', 'Нет']]
    general_issues = ['меньше 4 часов ', 'Нет', 'Нет', 'Нет']
    tmp_isserues = row[27:len(row)].copy()
    otvety = [[], []]
    tmp = [i for i, j in zip(komb[0], komb[1]) if i == j]
    otvety[0].append(len(tmp))
    otvety[1].append('Комбинаторика')
    tmp = [i for i, j in zip(teorver[0], teorver[1]) if i == j]
    otvety[0].append(len(tmp))
    otvety[1].append('Теорвер')
    tmp = [i for i, j in zip(matanaliz[0], matanaliz[1]) if i == j]
    otvety[0].append(len(tmp))
    otvety[1].append('Матанализ')
    tmp = [i for i, j in zip(lineyka[0], lineyka[1]) if i == j]
    otvety[0].append(len(tmp))
    otvety[1].append('Линейная Алгебра')
    tmp = [i for i, j in zip(algos[0], algos[1]) if i == j]
    otvety[0].append(len(tmp))
    otvety[1].append('Алгоритмы')
    res = []
    for i in range(0, 4):
        if general_issues[i] != tmp_isserues[i]:
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


def get_user_responses(sheet, user_col, telegram_login):
    return len(user_col) - rindex(user_col, telegram_login) - 1


def get_time(sheet, col_num, user_responses):
    time_col = sheet.col_values(col_num)
    if len(time_col) == 1:
        date_time_sheet = datetime.fromtimestamp(time.mktime(time.gmtime(0)))
    else:
        date_time_sheet = datetime.\
            strptime(sheet.col_values(1)[user_responses], '%d.%m.%Y %H:%M:%S')

    return date_time_sheet


def get_api(telegram_login, date_telegram_login):
    date_telegram_login += timedelta(hours=3)

    sheet = get_sheet()

    user_col = sheet.col_values(USER_NAME_COL_NUM)
    user_responses = get_user_responses(
        sheet, user_col, telegram_login)
    date_time_sheet = get_time(sheet, TIME_COL_NUM, user_responses)

    logger.info(
        f"Waiting for {telegram_login} form submission at {date_telegram_login}")

    while rindex(user_col, telegram_login) == -1 or date_time_sheet < date_telegram_login:
        time.sleep(5)
        date_time_sheet = get_time(sheet, TIME_COL_NUM, user_responses)
        user_col = sheet.col_values(USER_NAME_COL_NUM)
        user_responses = get_user_responses(
            sheet, user_col, telegram_login)

    row = sheet.row_values(user_responses + 1)
    igory, pashalki = result(row)
    pashalki_, comments_ = result_return(
        dictionary(), igory[0], igory[1], pashalki)

    pic_name = str(date_telegram_login) + telegram_login + '.png'
    graphs(pic_name, igory[0], igory[1])

    logger.info(
        f"Got it for {telegram_login} form submission at {date_telegram_login}")
    return pic_name, pashalki_, comments_


if __name__ == "__main__":
    get_api('bot6', datetime.today())
