import time
import gspread
import logging
import json
from graphs import graphs
from config import MODE, GOOGLE_API_TOKEN, TABLE_NAME, image_path
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - '
                           '%(levelname)s - %(message)s')
logger = logging.getLogger()

USER_NAME_COL_NUM = 2
TIME_COL_NUM = 1


# Функция принимает lst - список элементов и val - значение элемента
# Функция производит поиск последнего вхождения val в lst и возвращает
# индекс вхождения, если val в lst не найден, то возвращает -1
def rindex(lst, val):
    try:
        i = lst[::-1].index(val, 0, len(lst))
        return i
    except ValueError:
        return -1


# Функция принимает d - словарь, result_answers - список ответов, result_name -
# список названия разделов poshalky - список дополнительной информации от
# пользователя. Функция производит анализ количества полученных ответов от
# пользователя и возвращает по каждой плохо отвеченной теме рекомендации
def return_comments_for_user(d, result_answers, result_name, poshalky):
    study_recommendations = []
    general_recommendations = []
    for i in range(0, len(result_answers)):
        if result_answers[i] < 4:
            study_recommendations.extend(d[result_name[i]])
    if poshalky[0] == 1:
        general_recommendations.append(d['time'])
    if poshalky[1] == 1:
        general_recommendations.append(d['job'])
    if poshalky[2] == 1:
        general_recommendations.append(d['Deadlines'])
    if poshalky[3] == 1:
        general_recommendations.append(d['Лапки'])
    return general_recommendations, study_recommendations


# Функция содержит словарь: ключ - тема, значение - список рекомендаций
# Функция возвращет словарь
def dictionary():
    d = {'Комбинаторика': ['Так как Вы набрали небольшое количество баллов в разделе *Комбинаторика*, мы советуем Вам обратить внимание на данные курсы: ',
                           '\n1. [Ликбез по дискретной математике](https://stepik.org/course/91/syllabus)',
                           '2. [Основы перечислительной комбинаторики](https://stepik.org/course/125/promo)\n'],
         'Теорвер': ['Для комфортного обучения в нашей магистратуре Вам следует подтянуть *ТеорВер*. Вот наши рекомендации: ',
                    '\n1. [Теория вероятностей](https://stepik.org/course/3089/syllabus)',
                    '2. [Теория вероятности и статистика](https://www.coursera.org/browse/data-science/probability-and-statistics)\n'],
         'Матанализ': ['Чтобы подтянуть *Матанализ*, советуем изучить эти ресурсы:',
                       '\n1. [Математический анализ (часть 1)](https://stepik.org/course/716/syllabus)',
                       '2. [Математический анализ (часть 2)](https://stepik.org/course/711/promo)\n'],
         'Линейная Алгебра': ['Для успешной сдачи вступительных испытаний советуем вам ознакомиться с курсами по *Линейной алгебре*:',
                        '\n1. [Линейная алгебра (Linear Algebra)](https://www.coursera.org/learn/algebra-lineynaya)',
                        '2. [Линейная алгебра](https://stepik.org/course/2461/promo)\n'],
         'Алгоритмы': ['Мы оооочень рекомендуем Вам внимательно изучить данные курсы по *Алгоритмам и структурам данных*: ',
                       '\n1. [Алгоритмы: теория и практика. Методы](https://stepik.org/course/217/promo)',
                       '2. [Алгоритмы](https://www.coursera.org/browse/computer-science/algorithms)\n'],
         'time': 'Будьте готовы к тому, что из-за высокой интенсивности обучения, Вам придется *спать намного меньше*, чем Вы привыкли спать сейчас :)',
         'job': 'На нашем направлении слишком активная студенческая жизнь в плане учебы, поэтому Вам *НЕ удастся совмещать обучение с работой*.',
         'Deadlines': 'Если Вы любите откладывать все на потом, то будьте готовы к тому, что Вы столкнетесь с *большими проблемами*, так как каждый день Вам будет необходимо делать новую задачку, и если они вдруг накопятся....',
         'Лапки': 'Домашние работы на нашем направлении *сложнее в 100000 раз*, чем этот тест.'}
    return d


# Функция принимает row - список ответов пользователя на тест
# Функция сравнивает ответы пользователя с правильными и возвращает
# количество правильных ответов по каждой из тем
def result(row):
    # Парс ответов пользователя по отдельным темам
    komb = [row[2:7], ['3', '899076', '441', '371', '15625']]
    teorver = [row[7:12], ['11 216 28', 'да', '0.0116', '0.52', '6']]
    matanaliz = [row[12:17], ['0.0025', '-30.069', '-0.1489', '116', '5']]
    lineyka = [row[17:22], ['2', '0', '6', '3; 0', '(0.5; 1), (-1; 1)']]
    algos = [row[22:27], ['f3,f2,f4,f1', 'B', 'O(logn)', 'O(nlogn)', 'Нет']]

    # Наименования тем
    result_name = ['Комбинаторика', 'Теорвер', 'Матанализ', 'Линейная Алгебра',
                   'Алгоритмы']
    result_answers = [[komb], [teorver], [matanaliz], [lineyka], [algos]]
    otvety = [[], []]

    # Поэлементное сравнение ответов пользователя с идеальными
    for k in range(0, len(result_answers)):
        tmp = [i for i, j in zip(result_answers[k][0][0],
                                 result_answers[k][0][1]) if i == j]
        otvety[0].append(len(tmp))
        otvety[1].append(result_name[k])

    general_issues = ['меньше 4 часов ', 'Нет', 'Нет', 'Нет']
    tmp_isserues = row[27:len(row)].copy()
    result_general_information = []

    # "Анализ" дополнительной информации о пользователе
    for i in range(0, 4):
        if general_issues[i] != tmp_isserues[i]:
            result_general_information.append(1)
        else:
            result_general_information.append(0)
    return otvety, result_general_information


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


# Функция возвращает индекс строки ответов из Google Sheets
# если ответов от данного пользователя не поступала функция возвращает -1
def get_user_responses(sheet, user_col, telegram_login):
    if rindex(user_col, telegram_login) == -1:
        return -1
    return len(user_col) - rindex(user_col, telegram_login) - 1


# Функция переводит время окончания прохождения пользователем ответов
# из str в datetime функция веренет time.gmtime(0) если пользователь
# еще не прошел тест(ответы еще не появились в Google sheets или если
# пользователь уже проходил этот тест и хочет пройти еще раз, тогда мы
# должны убедиться, в том что полученные от него ответы это именно
# последние(после того как бот отправил ссылку)
def get_time(sheet, col_num, user_responses):
    time_col = sheet.col_values(col_num)
    if len(time_col) == 1 or user_responses == -1:
        date_time_sheet = datetime.fromtimestamp(time.mktime(time.gmtime(0)))
    else:
        date_time_sheet = datetime. \
            strptime(sheet.col_values(1)[user_responses], '%d.%m.%Y %H:%M:%S')
    return date_time_sheet


# Функция получает данные из Google sheets и отправляет результаты в бота
def get_api(telegram_login, date_telegram_login):
    date_telegram_login += timedelta(hours=3)

    sheet = get_sheet()

    user_col = sheet.col_values(USER_NAME_COL_NUM)
    user_responses = get_user_responses(sheet, user_col, telegram_login)
    date_time_sheet = get_time(sheet, TIME_COL_NUM, user_responses)

    logger.info(
        f"Waiting for {telegram_login} form submission at "
        f"{date_telegram_login}")

    while user_responses == -1 or date_time_sheet < date_telegram_login:
        time.sleep(5)
        date_time_sheet = get_time(sheet, TIME_COL_NUM, user_responses)
        user_col = sheet.col_values(USER_NAME_COL_NUM)
        user_responses = get_user_responses(
            sheet, user_col, telegram_login)

    row = sheet.row_values(user_responses + 1)
    result_for_graphix, comment_for_user = result(row)
    general_recommendations, study_recommendations = \
        return_comments_for_user(dictionary(), result_for_graphix[0],
                                 result_for_graphix[1], comment_for_user)
    logger.info(
        f"Drawing picture for {telegram_login} form submission at "
        f"{date_telegram_login}")

    path = image_path(date_telegram_login, telegram_login)
    graphs(path, result_for_graphix[0], result_for_graphix[1])

    logger.info(
        f"Got it for {telegram_login} form submission at {date_telegram_login}"
    )
    return path, general_recommendations, study_recommendations


if __name__ == "__main__":
    get_api('forsenlol1', datetime.fromtimestamp(time.mktime(time.gmtime(1000000))))
