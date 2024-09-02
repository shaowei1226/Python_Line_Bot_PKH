from flask import Flask, request, abort
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# 加載 .env 文件中的環境變量
load_dotenv()

# 連接到 MongoDB
client = MongoClient(os.getenv('MONGODB_URI'))
db = client['poker_hands']
collection = db['hands']
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import PostbackEvent
from dotenv import load_dotenv
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

@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    # 假設你從 data 中提取了所需的資料
    hand_data = {
        "Level": "5",
        "玩家人數": "6",
        "Hero 位置": "BTN",
        "Hero 後手": "2000",
        "其他玩家後手": "1500",
        "Hero 手牌": "As Ks",
        "翻前Action": "Raise",
        "Flop Cards": "Ah Kh 2d",
        "Flop Action": "Check",
        "Turn Card": "3c",
        "Turn Action": "Bet",
        "River Card": "4h",
        "River Action": "Call"
    }
    inserted_id = save_hand_data(hand_data)
    line_bot_api.reply_message(
        event.reply_token
    )

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
