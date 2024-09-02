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
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    if 'action=record_hand' in data:
        
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
        
    
    
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)