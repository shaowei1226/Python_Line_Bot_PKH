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

# 處理 Postback 事件
@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    if 'action=record_hand' in data:
        # 這裡可以解析 data 或者從中提取所需的 ID 等信息
        # 假設 SQL_ID 是你在 data 中的一部分
        sql_id = "12345"  # 這裡的 SQL_ID 應該從 data 中提取出來
        
        # 準備回覆訊息
        reply_message = f"紀錄已保存 id={sql_id}"

        # 回覆訊息給使用者
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )
        
    
    
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)