import sys
from io import BytesIO

from pymongo import MongoClient

import telegram
from flask import Flask, request, send_file
from transitions.extensions import GraphMachine

API_TOKEN = '470447162:AAGF3hkkIO5Ktbv0sbkDyG3dQ_m6e7HJmUs'
WEBHOOK_URL = 'https://2e143d6d.ngrok.io/hook'

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    def is_going_to_state1(self, update):
        text = update.message.text
        return text.lower() == 'sohai mou'

    def is_going_to_state2(self, update):
        text = update.message.text
        return text.lower() == 'go to state2'

    def is_going_to_state3(self, update):
        text = update.message.text
        return text.lower() == 'go to state3'

    def on_enter_state1(self, update):
        update.message.reply_text("Please enter the message you want to send to others")
        update.message.reply_text("Please enter according to this format")
        update.message.reply_text("SEND: (NAME) - YYY")

    def on_exit_state1(self, update):
        print('Leaving state1')

    def on_enter_state2(self, update):
        update.message.reply_text("Please enter ur name in this format ")
        update.message.reply_text("RECV: (NAME) - YYY")

    def on_exit_state2(self, update):
        print('Leaving state2')

    def on_enter_state3(self, update):
        update.message.reply_text("Please kindly give me ur opinion regarding")
        update.message.reply_text("this bot. Any opinion are appreciated")
        update.message.reply_text("OPOP:  YYY")

    def on_exit_state3(self, update):
        print('Leaving state3')

    def on_enter_state5(self, update):
        text = update.message.text
        print(text[6:9])

    def on_enter_user(self, update):
        update.message.reply_text("User")
        update.message.reply_text("Welcome to Xiong_Bot")
        update.message.reply_text("This is a place where you can leave")
        update.message.reply_text("message for others")
        print('Backed to user')

    def on_exit_user(self,update):
        print('not in init')

init = 1

client = MongoClient()
db = client.xiong
mycol = db.mycol

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=['user', 'state1', 'state2', 'state3', 'state4', 'state5', 'state6', 'state7'],
    transitions=[
        {
            'trigger': 'g_s1', 'source': 'user', 'dest': 'state1'
        },
        {
            'trigger': 'g_s2', 'source': 'user', 'dest': 'state2'
        },
        {
            'trigger': 'g_s3', 'source': 'user', 'dest': 'state3'
        },
        {
            'trigger': 'g_s4', 'source': 'user', 'dest': 'state4'
        },
        {
            'trigger': 'g_s5', 'source': 'state1', 'dest': 'state5'
        },
        {
            'trigger': 'g_s6', 'source': 'state2', 'dest': 'state6'
        },
        {
            'trigger': 'g_s7', 'source': 'state3', 'dest': 'state7'
        },
        {
            'trigger': 'go_back',
            'source': ['state1', 'state2', 'state3'],
            'dest': 'user'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    text = update.message.text
    if text == "/start" or text == "/restart":
        update.message.reply_text("Welcome to Xiong_Bot")
        update.message.reply_text("This is a place where you can leave")
        update.message.reply_text("message for others")
        print(machine.state)
        # (to receive)update.message.reply_text("Welcome to Xiong_Bot")
        # (to send)update.message.reply_text("Welcome to Xiong_Bot")
        # (leave opinion)update.message.reply_text("Welcome to Xiong_Bot")
    # elif text == "go back":
        # machine.go_back(update)

    # first OP
    elif text[0:4] == "SEND":
        machine.g_s5(update)

    elif text[0:4] == "RECV":
        machine.g_s6(update)

    elif text[0:4] == "OPOP":
        machine.g_s7(update)

    # change to button operation
    elif text.lower() == 'go to state1':
        machine.g_s1(update)
    elif text.lower() == 'go to state2':
        machine.g_s2(update)
    elif text.lower() == 'go to state3':
        machine.g_s3(update)

    else:
        update.message.reply_text(text)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    app.run()
