# TOC-2017-Telegram-Chatbot
A telegram chatbot implemented using python3

## How to run the chatbot
1.Prepare a computer with debian-based OS installed (ex.Ubuntu)__
2.run all the command listed in install.txt in the correct order, **order matters**__
3.download ngrok to your computer and run with__
>./ngrok http 5000
4.open mongo shell in bash__
>mongo
5.type in the following commands to build the necessary database and collections__
>use TOC
>db.createCollection("comment")
>db.createCollection("opinions")
6.change the API-TOKEN and WEBHOOK-URL section in the app.py__
7.run with python3 app.py__
