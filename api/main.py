from pprint import pprint
from oauth2client.service_account import ServiceAccountCredentials
import gspread

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def main():
    scope = ["https://spreadsheets.google.com/feeds",
             'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.\
        from_json_keyfile_dict(GOOGLE_API_KEY, scope)
    client = gspread.authorize(creds)
    sheet = client.open("Tests").sheet1

    data = sheet.get_all_records()

    number_row = 3
    number_col = 2

    row = sheet.row_values(number_row)
    col = sheet.col_values(number_col)
    cell = sheet.cell(number_row, number_col).value

    pprint(data)
    pprint(row)
    pprint(col)
    pprint(cell)


if __name__ == "__main__":
    main()

