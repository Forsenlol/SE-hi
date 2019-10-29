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

    data = sheet.get_all_records()

    user_col = sheet.col_values(USER_NAME_COL_NUM)
    user_responses = len(user_col) - rindex(user_col, telegram_login)

    time_col = sheet.col_values(TIME_COL_NUM)  
    if len(time_col) == 1:
        date_time_sheet = datetime.fromtimestamp(time.mktime(time.gmtime(0)))
    else:
        date_time_sheet = datetime.\
            strptime(sheet.col_values(1)[user_responses], '%d.%m.%Y %H:%M:%S')

    logger.info(f"Waiting for {telegram_login} form submission at {date_telegram_login}")
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

    logger.info(f"Got it for {telegram_login} form submission at {date_telegram_login}")
    return sheet.row_values(user_responses)


if __name__ == "__main__":
    get_api('bot6')

