from pprint import pprint
import time
from oauth2client.service_account import ServiceAccountCredentials
import gspread


# Функция для поиска индекса последнего вхождения значения val в список
def rindex(lst, val):
    try:
        i = lst[::-1].index(val, 0, len(lst))
        return i
    except ValueError:
        return -1


def get_api(telegram_log):
    scope = ["https://spreadsheets.google.com/feeds",
             'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.\
        from_json_keyfile_name('SoftwareEngineering.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("Tests").sheet1

    data = sheet.get_all_records()

    number_col = 2
    col = sheet.col_values(number_col)
    user_responses = len(col) - rindex(col, telegram_log)
    while rindex(col, telegram_log) == -1:
        time.sleep(5)
        col = sheet.col_values(number_col)
        user_responses = len(col) - rindex(col, telegram_log)
    # cell = sheet.cell(number_row, number_col).value
    row = sheet.row_values(user_responses)
    pprint(row[2:])
    # pprint(data)

    # Тут что то происходит


if __name__ == "__main__":
    get_api('bot6')

