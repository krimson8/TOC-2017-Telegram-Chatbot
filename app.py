import sys
from io import BytesIO

from pymongo import MongoClient

import telegram
from flask import Flask, request, send_file
from transitions.extensions import GraphMachine

API_TOKEN = '470447162:AAGF3hkkIO5Ktbv0sbkDyG3dQ_m6e7HJmUs'
WEBHOOK_URL = 'https://5beb5005.ngrok.io/hook'

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    # def is_going_to_state1(self, update):
    #     text = update.message.text
    #     return text.lower() == 'sohai mou'
    #
    # def is_going_to_state2(self, update):
    #     text = update.message.text
    #     return text.lower() == 'go to state2'
    #
    # def is_going_to_state3(self, update):
    #     text = update.message.text
    #     return text.lower() == 'go to state3'

    def on_enter_state1(self, update):
        update.message.reply_text("Please enter the message you want to send to others\n" +
                                  "enter according to this format\n" +
                                  "SEND:(NAME)-YYY \nwhich the name should be three character\n" +
                                  "either chinese or english\n" +
                                  "followed by a dash and YYY is the content")

    def on_exit_state1(self, update):
        print('Leaving state1')

    def on_enter_state2(self, update):
        update.message.reply_text("Please enter ur name in this format\n" +
                                  "RECV:(NAME)\nwhich the name should be three character\n" +
                                  "either chinese or english")

    def on_exit_state2(self, update):
        print('Leaving state2')

    def on_enter_state3(self, update):
        update.message.reply_text("Please enter ur opinion in this format\n" +
                                  "OPOP:(CONTENT)\nwhich the CONTENT can be whatever\n")

    def on_exit_state3(self, update):
        print('Leaving state3')

    def on_enter_state4(self, update):
        machine.get_graph().draw("state_diagram.png", prog="dot")
        update.message.reply_photo(open("state_diagram.png", "rb"))
        # bot.send_photo(chat_id=chat_id, photo=open('state_diagram.png', 'rb'))
        for post in col2.find():
            x = post
            for k, v in x.items():
                if k == "opinion":
                    print("Message: " + v)
                    update.message.reply_text("Message: " + v)
        self.go_back(update)

    def on_enter_state5(self, update):
        text = update.message.text
        name = text[5:8]
        content = text[9:]
        print(name + ": " + content)
        post = {"name": name, "content": content}
        col.insert_one(post).inserted_id
        self.done_func(update)

    def on_enter_state6(self, update):
        text = update.message.text
        name = text[5:8]
        print(name)
        for post in col.find({"name": name}):
            x = post
            for k, v in x.items():
                if k == "content":
                    print("Message: " + v)
                    update.message.reply_text("Message: " + v)
        self.done_func(update)

    def on_enter_state7(self, update):
        text = update.message.text
        opinion = text[5:]
        print(opinion)
        post = {"opinion": opinion}
        col2.insert_one(post).inserted_id
        self.done_func(update)

    def on_enter_user(self, update):
        update.message.reply_text("User")
        update.message.reply_text("Welcome to Xiong_Bot \nThis is a place where you can leave\nmessage for others")
        update.message.reply_text("Type the follow command to use the bot\n" +
                                  "1. gs1 (leave message for others)\n" +
                                  "2. gs2 (receive ur messages)\n" +
                                  "3. gs3 (leave opinion for me)\n" +
                                  "4. gs4 (show all the opinion and states diagram)")
        print('Backed to user')

    def on_exit_user(self, update):
        print('not in user')


client = MongoClient('mongodb://localhost:27017')
db = client.TOC
col = db.comment
col2 = db.opinion

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
            'source': ['state1', 'state2', 'state3', 'state4'],
            'dest': 'user'
        },
        {
            'trigger': 'done_func',
            'source': ['state5', 'state6', 'state7'],
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
    print(text)
    if text == "/start" or text == "/restart":
        update.message.reply_text("Welcome to Xiong_Bot \nThis is a place where you can leave\nmessage for others")
        update.message.reply_text("Type the follow command to use the bot\n" +
                                  "1. gs1 (leave message for others)\n" +
                                  "2. gs2 (receive ur messages)\n" +
                                  "3. gs3 (leave opinion for me)\n" +
                                  "4. gs4 (show all the opinion and states diagram)")

    # first OP
    elif text[0:4].lower() == "send" and machine.state == "state1":
        machine.g_s5(update)

    elif text[0:4].lower() == "recv" and machine.state == "state2":
        machine.g_s6(update)

    elif text[0:4].lower() == "opop" and machine.state == "state3":
        machine.g_s7(update)

    # change to button operation
    elif text.lower() == 'gs1':
        machine.g_s1(update)
    elif text.lower() == 'gs2':
        machine.g_s2(update)
    elif text.lower() == 'gs3':
        machine.g_s3(update)
    elif text.lower() == 'gs4':
        machine.g_s4(update)

    else:
        update.message.reply_text(text)

    text = ""
    print(machine.state)
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
