# TOC-2017-Telegram-Chatbot
A telegram chatbot implemented using python3

## How to run the chatbot
1.Prepare a computer with debian-based OS installed (ex.Ubuntu)<br />
2.run all the command listed in install.txt in the correct order, **order matters**<br />
3.download ngrok to your computer and run with<br />
<pre>./ngrok http 5000</pre>
4.open mongo shell in bash<br />
<pre>mongo</pre>
5.type in the following commands to build the necessary database and collections<br />
<pre>use TOC</pre>
<pre>db.createCollection("comment")</pre>
<pre>db.createCollection("opinions")</pre>
6.change the API-TOKEN and WEBHOOK-URL section in the app.py<br />
7.run with python3 app.py<br />
