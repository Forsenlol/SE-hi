import os

TOKEN = os.getenv("TOKEN")
PORT = os.getenv("PORT")
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")
MODE = os.getenv("MODE")
GOOGLE_FORM_URL = os.getenv("GOOGLE_FORM_URL")
GOOGLE_API_TOKEN = os.getenv("GOOGLE_API_TOKEN")
TABLE_NAME = os.getenv("TABLE_NAME")

PHOTO_PATH = ['data/photos/']


def image_path(date, login):
    pic_name = str(date) + login + '.png'
    pic_name = pic_name.replace(':', '_')
    return pic_name