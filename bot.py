import logging
import sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import TOKEN, PORT, HEROKU_APP_NAME, MODE
import requests

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


if MODE == "prod":
    def run():
        updater.start_webhook(listen="0.0.0.0",
                                port=PORT,
                                url_path=TOKEN)
        updater = Updater(TOKEN, use_context=True)

        updater.dispatcher.add_handler(CommandHandler("start", start))
        updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
else:
    def run():
        get_request = requests.get('http://pubproxy.com/api/proxy?limit=1&'
                               'format=txt&port=8080&level=anonymous&'
                               'type=socks5&country=FI|NO|US&https=True')
        updater = Updater(TOKEN, use_context=True, request_kwargs={'proxy_url': f'https://{get_request.text}'})

        updater.dispatcher.add_handler(CommandHandler("start", start))
        updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))

        updater.start_polling()


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Hi! I\'m SE-Hi bot')


def echo(update, context):
    response = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=response)


if __name__ == '__main__':
    logger.info("Starting bot")
    run()
