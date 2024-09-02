

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, PostbackEvent
from dotenv import load_dotenv
from pymongo import MongoClient
import os

app = Flask(__name__)
load_dotenv()
line_bot_api = LineBotApi(os.getenv('LINE_BOT_API'))
handler = WebhookHandler(os.getenv('HANDLER_SECRET'))

# 連接到 MongoDB
client = MongoClient(os.getenv('MONGODB_URI'))
db = client['poker_hands']
collection = db['hands']

def save_hand_data(data):
    document = {
        "Level": data.get("Level", ""),
        "玩家人數": data.get("玩家人數", ""),
        "Hero 位置": data.get("Hero 位置", ""),
        "Hero 後手": data.get("Hero 後手", ""),
        "其他玩家後手": data.get("其他玩家後手", ""),
        "Hero 手牌": data.get("Hero 手牌", ""),
        "翻前Action": data.get("翻前Action", ""),
        "Flop Cards": data.get("Flop Cards", ""),
        "Flop Action": data.get("Flop Action", ""),
        "Turn Card": data.get("Turn Card", ""),
        "Turn Action": data.get("Turn Action", ""),
        "River Card": data.get("River Card", ""),
        "River Action": data.get("River Action", ""),
    }
    result = collection.insert_one(document)
    return result.inserted_id

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    message_text = event.message.text

    # 將使用者傳送的資料存入 MongoDB
    poker_hand_data = {
        "user_id": user_id,
        "data": message_text
    }
    collection.insert_one(poker_hand_data)

    # 回應使用者
    reply_message = TextSendMessage(text="資料已儲存！")
    line_bot_api.reply_message(event.reply_token, reply_message)

@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    if 'action=record_hand' in data:
        # 處理手牌紀錄的 Postback 事件
        reply_message = TextSendMessage(text="請填寫以下資料：\nLevel: \n玩家人數: \nHero 位置: \nHero 後手: \n其他玩家後手: \nHero 手牌: \n翻前Action: \nFlop Cards: \nFlop Action: \nTurn Card: \nTurn Action: \nRiver Card: \nRiver Action:")
        line_bot_api.reply_message(event.reply_token, reply_message)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
