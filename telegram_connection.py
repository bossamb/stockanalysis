import telegram
from telegram.ext import Updater, MessageHandler, Filters
# import schedule
import time
from bs4 import BeautifulSoup as bs
import requests
import datetime
from telegram import ChatAction
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler

def message_ctrl(update, context):
    print(update.message)
    update.message.reply_text('hi')


def telegram_connection():
    print('activate telegram connection')
    updater = Updater("1941923189:AAEmoXlilPt2PpK2qXPH8-3Ya2bVH880ZXs", use_context=True)
     # define updater
    message_handler = MessageHandler(Filters.text, message_ctrl)
    updater.dispatcher.add_handler(message_handler)
    updater.start_polling()
    updater.stop()

def main():
    telegram_connection()

if __name__ == '__main__':
    main()
    print('aaaa')


# dispatcher = updater.dispatcher
# #dispatcher 는 이벤트 왔을때 처리해줄수 있는 객체 입니다.
# #아래와 같이 start 함수를 만들어 놓습니다.
# def start(bot, update):
#     bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
# from telegram.ext import CommandHandler
# start_handler = CommandHandler('start', start)
# dispatcher.add_handler(start_handler)
# updater.start_polling()
#여기서 CommandHandler 는 /start 메세지 를 들어 올때는 의미합니다 / 가 붙으면 커맨더 명령이라고 인식 합니다.
# 그리고 dispatcher 에 해당 핸들러를 추가 해 줍니다.
# 그럼/start 채팅이 홨을때 update.message.chat_id-> /start 메세지를 보낸 ID 에
# "I'm a bot, please talk to me!" 을 보냅니다.






#
#
#
#
# #
# #
# # def cb_button(update, context):
# #     query = update.callback_query
# #     data = query.data
# #
# #     context.bot.send_chat_action(
# #         chat_id=update.effective_user.id
# #         , action=ChatAction.TYPING
# #     )
# #     context.bot.edit_message_text(
# #         text='[{}] 작업을 완료하였습니다.'.format(data)
# #         , chat_id=query.message.chat_id
# #         , message_id=query.message.message_id
# #     )
#
#
# # def job():
# #     now = time.localtime()
# #     telegram_sending(get_headlines())
# #     print("current time = ", str(now))
#
# def telegram_sending(stuffs):
#     # send stuff to telegram
#     token = "1941923189:AAEmoXlilPt2PpK2qXPH8-3Ya2bVH880ZXs"
#     bot = telegram.Bot(token=token)
#     chat_id = "1777070088"
#     text = stuffs
#     bot.sendMessage(chat_id=chat_id, text=text)
#
# def get_headlines():
#     # get headlines with bs4
#     url = 'https://news.naver.com/main/home.naver'
#     headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
#                 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
#     response = requests.get(url, headers=headers)
#     html_text = response.text
#     soup = bs(html_text, 'html.parser')
#     headlines = soup.find_all('div', {'class': 'hdline_article_tit'})
#     to_send = f"{datetime.datetime.now().strftime('%Y-%m-%d %H')}시 HeadLine News \n\n"
#     for i, d in enumerate(headlines):
#         to_send += f"{i+1}. {d.get_text().strip()} \n\t : https://news.naver.com{d.find('a')['href']} \n "
#     return to_send
#
#
# def get_message(update, context):
#     # check function availability
#     if update.message.text == '뉴스':
#         telegram_sending(get_headlines())
#     elif update.message.text == '주가':
#         update.message.reply_text("Enter the stock you want to search: ")
#         name = finance.get_stock_name(update.message.text)
#     else:
#         upate.message.reply_text('유효한 명령어를 호출해주세요 \n\t ex) 뉴스')
#
# def to_telegram():
#     updater = Updater("1941923189:AAEmoXlilPt2PpK2qXPH8-3Ya2bVH880ZXs", use_context=True)
#     message_handler = MessageHandler(Filters.text, get_message)
#     updater.dispatcher.add_handler(message_handler)
#     updater.start_polling()
#
#
# # command hander
# def start(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
#
# updater = Updater(token=token, use_context=True)
# dispatcher = updater.dispatcher
# start_handler = CommandHandler('start', start)
# dispatcher.add_handler(start_handler)
#
# def
#
# def main():
#     print('Starting')
#     updater = Updater("1941923189:AAEmoXlilPt2PpK2qXPH8-3Ya2bVH880ZXs", use_context=True)
#     message_handler = MessageHandler(Filters.text, get_message)
#     updater.dispatcher.add_handler(message_handler)
#     updater.start_polling()
#     updater.idle()
#
#     # schedule.every().day.at("1:02").do(job)
#     # while True:
#     #     schedule.run_pending()
#     #     time.sleep(1)
#