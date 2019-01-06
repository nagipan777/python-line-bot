from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

app = Flask(__name__)

line_bot_api = LineBotApi('d4hzbgIVZJ98UeOlKaqP0/aROFMuNKIB9Pec+Ooz0uqzmrUXtiVNvaD23/rEAuttiOI2KngiB6Oe1TiirYe6vQZQdoW3oeOs8el1l+OcmXa/NCFk8bNuXa7gyXyBHYHNZjAIlD5U616PdfEYA/8P9AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f7e4b43f3dbd16761859c2910ca93deb')

# @app.route("/")
# def hello_world():
#   return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
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


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)