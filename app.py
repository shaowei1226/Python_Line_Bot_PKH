from flask import Flask, request, abort , jsonify

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from mongodb_function import *
from dotenv import load_dotenv
import os
import requests
import json

from linebot import (
    LineBotApi, WebhookHandler
)
from pymongo import MongoClient

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(os.getenv('line_bot_api'))
# Channel Secret
handler = WebhookHandler(os.getenv('handler'))

client = MongoClient(os.getenv('MONGODB_URI'))
db = client['poker_hands']  # 假設你的資料庫名稱為 poker_hands_db
collection = db['hands']  # 假設你的集合名稱為 hands

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    write_one_data(eval(body.replace('false','False')))
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if '手牌紀錄' in msg:  
        line_bot_api.reply_message(event.reply_token)       
    elif '@讀取' in msg:
        datas = read_many_datas()
        datas_len = len(datas)
        message = TextSendMessage(text=f'資料數量，一共{datas_len}條')
        line_bot_api.reply_message(event.reply_token, message)  

    elif '@查詢' in msg:
        datas = col_find('events')
        message = TextSendMessage(text=str(datas))
        line_bot_api.reply_message(event.reply_token, message)
        
    else:
        message = TextSendMessage(text=msg)
        line_bot_api.reply_message(event.reply_token, message)

@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)