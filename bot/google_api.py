import time
import gspread
import os
import logging
import json
from config import MODE, GOOGLE_API_TOKEN, TABLE_NAME
from oauth2client.service_account import ServiceAccountCredentials


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Функция для поиска индекса последнего вхождения значения val в список
def rindex(lst, val):
    try:
        i = lst[::-1].index(val, 0, len(lst))
        return i
    except ValueError:
        return -1


def get_api(telegram_log, date_telegram_log):
    scope = ["https://spreadsheets.google.com/feeds",
             'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        json.loads(GOOGLE_API_TOKEN), scope)
    logger.info("Getting credentials")

    client = gspread.authorize(creds)
    sheet = client.open(TABLE_NAME).sheet1

    data = sheet.get_all_records()

    number_col = 2
    col = sheet.col_values(number_col)
    user_responses = len(col) - rindex(col, telegram_log)

    logger.info(f"Waiting for {telegram_log} form submission")
    while rindex(col, telegram_log) == -1:
        time.sleep(5)
        col = sheet.col_values(number_col)
        user_responses = len(col) - rindex(col, telegram_log)
    row = sheet.row_values(user_responses)
    logger.info("Got it")

    return row


if __name__ == "__main__":
    get_api('bot6')

