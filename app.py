from pymongo import MongoClient
import os
from flask import Flask, request, abort
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage

app = Flask(__name__)

load_dotenv()

client = MongoClient(os.getenv('MONGODB_URI'))
db = client['poker_hands']
collection = db['hands']

line_bot_api = LineBotApi(os.getenv('line_bot_api'))
handler = WebhookHandler(os.getenv('handler'))

print(os.getenv('line_bot_api'))
print(os.getenv('handler'))
print(os.getenv('MONGODB_URI'))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("Received a message")
    
    user_message = {
        'user_id': event.source.user_id,
        'message': event.message.text,
        'timestamp': event.timestamp
    }
    
    try:
        collection.insert_one(user_message)
        print("Message saved to MongoDB")
    except Exception as e:
        print(f"Failed to save message to MongoDB: {e}")
    
    line_bot_api.reply_message(
        event.reply_token,
        TextMessage(text=f"你說了: {event.message.text}")
    )

if __name__ == "__main__":
    app.run(port=8000)
