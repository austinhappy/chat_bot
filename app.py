#接收和回復機器人
#建立與LINE機器的頁面
#SDK(software development kit)
#line-bot-sdk-python 軟體開發套件
#主程式會寫app.py
#flask, django是目前主流的伺服器開發方式，django是專為設計網頁用的

#########################
########架設伺服器########
#########################
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

app = Flask(__name__)

line_bot_api = LineBotApi('WewrORTBgH0yCQR9WjAOnn/d/+IDbyDD2IZ7aTgDIDxG6UFP047mBKf0tEwaIfiTSuwl2xjwAY4Hn274KVTSnNKmyowDwkH+T5i93R6jBVAiiUfXHiQbiUwJHlDLha6TNcaI2dl1SLIvsym2ihOfTwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2b515c331478b8ab14c8a226edd88d73')


@app.route("/callback", methods=['POST']) #有人要用某網址連結近來才會觸發此程式
#接受來自LINE傳來的訊息
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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text #使用者傳來的訊息
    r = '你說啥?'

    if msg in ['hi', 'Hi']:
        r = '哈囉!'
    elif msg == '你吃飯了嗎?':
        r = '還沒'
    elif msg == '你是誰':
        r = '我是機器人'
    elif '訂位' in msg:
        r = '你想要訂位嗎?'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r)) #event.message.text回復傳來的訊息


if __name__ == "__main__": #此行的用意是為了確保我們是寫執行的程式，而不是在import時就已經被執行各種有的沒的(CPU會跑很多沒意義的程式)
    app.run()
