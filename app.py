from flask import Flask, request, abort , jsonify

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from dotenv import load_dotenv
import os
import requests
import json
from linebot import (
    LineBotApi, WebhookHandler
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(os.getenv('line_bot_api'))
# Channel Secret
handler = WebhookHandler(os.getenv('handler'))

# 監聽所有來自 /callback 的 Post Request
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
    user_message = event.message.text
    if user_message == "手牌紀錄":
        # 格式化的手牌記錄模板
        reply_message = (
            "Level: \n"
            "玩家人數: \n"
            "Hero 位置: \n"
            "Hero 後手: \n"
            "其他玩家後手: \n\n"
            "Hero 手牌: \n"
            "翻前Action: \n"
            "Flop 開的牌: \n"
            "Flop Action: \n"
            "Turn 開的牌: \n"
            "Turn Action: \n"
            "River 開的牌: \n"
            "River Action: \n"
        )
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )
    
    
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)