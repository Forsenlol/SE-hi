import logging
import sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import TOKEN, PORT, HEROKU_APP_NAME, MODE

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

all_users = {}

def get_api(username):
    ...

if MODE == "prod":
    def run():
        updater = Updater(TOKEN, use_context=True)
        updater.start_webhook(listen="0.0.0.0",
                                port=PORT,
                                url_path=TOKEN)

        updater.dispatcher.add_handler(CommandHandler("start", start))
        updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
else:
    def run():
        import requests
        get_request = requests.get('http://pubproxy.com/api/proxy?limit=1&'
                               'format=txt&port=8080&level=anonymous&'
                               'type=socks5&country=FI|NO|US&https=True')
        updater = Updater(TOKEN, use_context=True, request_kwargs={'proxy_url': f'https://{get_request.text}'})

        updater.dispatcher.add_handler(CommandHandler("start", start))
        updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

        updater.start_polling()


def start(update, context):
    chat_id = update.effective_chat.id
    username = update.effective_user.name
    if chat_id not in all_users:
        all_users[chat_id] = username

    start_text = (f'Привет {update.effective_user.first_name}! '
                  'Данный бот поможет Вам понять, готовы ли Вы обучаться '
                  'на магистерской программе Software Engineering в ИТМО. '
                  f'Пройдите, пожалуйста, тест в Google Form по ссылке '
                  'https://forms.gle/ezkmBjgpUwxFFtyg8')

    get_api(username)
    context.bot.send_message(chat_id=chat_id,
                             text=start_text)


def echo(update, context):
    response = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=response)


if __name__ == '__main__':
    logger.info("Starting bot")
    run()
