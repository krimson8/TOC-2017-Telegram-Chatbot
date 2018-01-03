# TOC-2017-Telegram-Chatbot
A telegram chatbot implemented using python3

## How to run the chatbot
1.Prepare a computer with debian-based OS installed (ex.Ubuntu)<br />
2.run all the command listed in install.txt in the correct order, **order matters**<br />
3.download ngrok to your computer and run with<br />
>./ngrok http 5000
4.open mongo shell in bash<br />
>mongo
5.type in the following commands to build the necessary database and collections<br />
>use TOC
>db.createCollection("comment")
>db.createCollection("opinions")
6.change the API-TOKEN and WEBHOOK-URL section in the app.py<br />
7.run with python3 app.py<br />
