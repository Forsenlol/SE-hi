import logging
import sys
from google_api import get_api, get_all_users
from telegram.ext import run_async, Updater, CommandHandler, MessageHandler, \
    Filters
from telegram import ParseMode
from config import TOKEN, PORT, HEROKU_APP_NAME, MODE, GOOGLE_FORM_URL
from multiprocessing import Process

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


if MODE == "prod":
    def run():
        updater = Updater(TOKEN, use_context=True)
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)

        updater.dispatcher.add_handler(CommandHandler("start", start))
        updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

        updater.bot.set_webhook(
            "https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
elif MODE == "dev":
    def run():
        import requests
        get_request = requests.get('http://pubproxy.com/api/proxy?limit=1&'
                                   'format=txt&port=8080&level=anonymous&'
                                   'type=socks5&country=FI|NO|US&https=True')

        logger.info(f"Using proxy: {get_request.text}")
        # Current working proxy: 157.245.56.246:8080
        # updater = Updater(TOKEN, use_context=True, request_kwargs={
        #                   'proxy_url': f'https://{get_request.text}'})
        updater = Updater(TOKEN, use_context=True, request_kwargs={
                            'proxy_url': f'https://157.245.56.246:8080'})
        updater.dispatcher.add_handler(CommandHandler("start", start))
        updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

        updater.start_polling()
else:
    logger.error('No MODE specified')
    exit(1)


all_users = {}
@run_async
def start(update, context):
    chat_id = update.effective_chat.id
    username = update.effective_user.name[1:] # Without @
    if chat_id not in all_users:
        all_users[chat_id] = username

    start_text = (f'Привет, {update.effective_user.first_name}! '
                  'Данный бот поможет Вам понять, готовы ли Вы обучаться '
                  'на магистерской программе *Software Engineering* в ИТМО. '
                  f'Пройдите, пожалуйста, тест в '
                  f'[Google Form]({GOOGLE_FORM_URL}?entry.1107499763={username}).')

    context.bot.send_message(parse_mode=ParseMode.MARKDOWN,
                             chat_id=chat_id,
                             text=start_text)

    data = get_api(username, update.effective_message.date)
    context.bot.send_message(chat_id=chat_id, text=data)


def echo(update, context):
    response = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=response)


if __name__ == '__main__':
    logger.info("Starting bot")
    run()
