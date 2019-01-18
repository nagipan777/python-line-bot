from flask import Flask, render_template, request, jsonify, abort
import os
import sys
import json
import urllib.request, urllib.parse
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)


app = Flask(__name__)

channel_secret = os.getenv('YOUR_CHANNEL_SECRET', None)
channel_access_token = os.getenv('YOUR_CHANNEL_ACCESS_TOKEN', None)

if channel_secret is None:
    print('Specify YOUR_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify YOUR_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

   # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     data = {
#         "apikey" : DZZfRUiqAVPaWAohiTypko0kJpIVSChz,
#         "query": event.message.text
#     }
#     data = urllib.parse.urlencode(data).encode("utf-8")
#     with urllib.request.urlpoen("https://api.a3rt.recruit-tech.co.jp/talk/v1/smalltalk", data=data) as res:
#         reply_json = json.loads(res.read().decode("unicode_escape"))
#         if reply_json['status'] == 0:
#             reply = reply_json['results'][0]['reply']
#             line-bot-api.reply_message(
#                 event.reply_token,
#                 TextSendMessage(text=reply())


if __name__ == '__main__':
    #app.run()
     port = int(os.getenv("PORT", 5000))
     app.run(host="0.0.0.0", port=port)