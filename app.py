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

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    if 'action=record_hand2' in data:
        # 紀錄使用者傳送的訊息到 MongoDB
        user_id = event.source.user_id
        message = event.postback.fill_in_text
        
        record = {
            "user_id": user_id,
            "message": message
        }
        
        collection.insert_one(record)
        
        reply_message = "已紀錄手牌資料"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))


    
    
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)