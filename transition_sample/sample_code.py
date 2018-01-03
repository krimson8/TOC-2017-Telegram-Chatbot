import sys

import telegram
from flask import Flask, request

app = Flask(__name__)
bot = telegram.Bot(token='470447162:AAGF3hkkIO5Ktbv0sbkDyG3dQ_m6e7HJmUs')


def _set_webhook():
    status = bot.set_webhook('https://5ba04fe5.ngrok.io/hook')
    if not status:
        print('Webhook setup failed')
        sys.exit(1)


@app.route('/hook', methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        text = update.message.text
        print(text)
        update.message.reply_text(text)
    return 'ok'


if __name__ == "__main__":
    _set_webhook()
    app.run(port=6789)
