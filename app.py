from pymongo import MongoClient
import os
# 替換成你的 MongoDB 連接字串
client = MongoClient(os.getenv('MONGODB_URI'))
db = client['line_bot']
collection = db['messages']


from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage

app = Flask(__name__)

# 替換成你的 Line Bot 的 Channel Access Token 和 Channel Secret
line_bot_api = LineBotApi(os.getenv('line_bot_api'))
handler = WebhookHandler(os.getenv('handler'))

@app.route("/callback", methods=['POST'])
def callback():
    # 獲取簽名
    signature = request.headers['X-Line-Signature']

    # 獲取請求正文
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 驗證簽名並處理事件
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 保存用戶的對話內容到 MongoDB
    user_message = {
        'user_id': event.source.user_id,
        'message': event.message.text,
        'timestamp': event.timestamp
    }
    collection.insert_one(user_message)

    # 回覆用戶的消息
    line_bot_api.reply_message(
        event.reply_token,
        TextMessage(text=f"你說了: {event.message.text}")
    )

if __name__ == "__main__":
    app.run(port=8000)
