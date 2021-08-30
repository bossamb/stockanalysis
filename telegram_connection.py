# coding=utf-8
import telegram
from telegram.ext import Updater, MessageHandler, CommandHandler, ConversationHandler, Filters
import logging
# import schedule
import time
from bs4 import BeautifulSoup as bs
import requests
import datetime
from telegram import ChatAction
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler
import pandas_datareader.data as pdweb
from pandas_datareader import data as pdr
# import yfinance # must pip install first
import seaborn as sns
import matplotlib.pyplot as plt
from selenium import webdriver

STOCK_NAME = 0
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_stock_data(name, start_date=(datetime.datetime.today() - datetime.timedelta(weeks=8)).strftime('%Y-%m-%d'),
                   end_date=datetime.datetime.today().strftime('%Y-%m-%d')):
    data = pdr.get_data_yahoo(name, start_date, end_date)
    return data

def get_stock_name(name):
    try:
        stock_name = name
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        URL = 'https://www.naver.com/'
        driver = webdriver.Chrome(executable_path='/Users/yh/Pycharm/Stuffs/chromedriver', options=options)
        driver.get(url=URL)
        driver.find_element_by_xpath('//*[@id="query"]').send_keys(stock_name)
        driver.find_element_by_xpath('//*[@id="search_btn"]/span[2]').click()
        item = []
        item.append(driver.find_element_by_xpath('//*[@id="_cs_root"]/div[1]/div/h3/a/span[1]').text)
        item.append(driver.find_element_by_xpath('//*[@id="_cs_root"]/div[1]/div/h3/a/em').text)
        item.append(driver.find_element_by_xpath('//*[@id="_cs_root"]/div[2]/div[2]/div/ul[1]/li[7]/a/dl/dt').text)
        # print(item)
        driver.quit()
        if item[2] == '코스피':
            item[2] = 'KS'
        else:
            item[2] = 'KQ'
        item[1] = f'{item[1]}.{item[2]}'
        return item[:2]
    except:
        logger.warning('검색에 실패했습니다.')

def message_ctrl(update, context):
    update.message.reply_text('hi')

def f_keyboarding(update, context):
    bot = telegram.Bot(token="1941923189:AAEmoXlilPt2PpK2qXPH8-3Ya2bVH880ZXs")  # bot을 선언
    custom_keyboard = [['/news', 'top-right'],  ['/stock', '/???'], ['/kbdoff', '/quit']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    bot.send_message(chat_id="1777070088", text="Custom Keyboard ON",  reply_markup=reply_markup)

def f_unkeyboarding(update, context):
    logger.info(f"{update.message.text} started")
    bot = telegram.Bot(token="1941923189:AAEmoXlilPt2PpK2qXPH8-3Ya2bVH880ZXs")  # bot을 선언
    reply_markup = telegram.ReplyKeyboardRemove()
    bot.send_message(chat_id="1777070088", text="Custom Keyboard OFF", reply_markup=reply_markup)

def get_headlines():
    # get headlines with bs4
    url = 'https://news.naver.com/main/home.naver'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
                (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    response = requests.get(url, headers=headers)
    html_text = response.text
    soup = bs(html_text, 'html.parser')
    headlines = soup.find_all('div', {'class': 'hdline_article_tit'})
    to_send = f"{datetime.datetime.now().strftime('%Y-%m-%d %H')}시 HeadLine News \n\n"
    for i, d in enumerate(headlines):
        to_send += f"{i+1}. {d.get_text().strip()} \n\t : https://news.naver.com{d.find('a')['href']} \n "
    return to_send

def f_news(update, context):
    logger.info(f"{update.message.text} started")
    update.message.reply_text(get_headlines())

def f_quit(update, context):
    logger.info(f"{update.message.text} started")
    update.message.reply_text('quit function')

def f_stock(update, context):
    logger.info(f"{update.message.text} started")
    update.message.reply_text('검색하려는 종목을 입력해주세요\n\t (ex. 삼성전자, LG화학)')
    return STOCK_NAME

def stock_name(update, context):
    """Stores the info about the user and ends the conversation."""
    logger.info(f"stockname to find is {update.message.text}")
    stock_searched = get_stock_name(update.message.text)
    logger.info(f"stockname to found is {stock_searched}")
    if stock_searched != None:
        stock_df = get_stock_data(stock_searched[1])
        logger.info(f'get_stock_data(stock_searched[1]) is \n{stock_df}')
        for i in range(-5, 0, 1):
            update.message.reply_text(f"At Date {stock_df.index[i].strftime('%Y-%m-%d')}\n "
                                      # f"LOW: {stock_df.iloc[i, 1]}, HIGH: {stock_df.iloc[i, 0]}\n "
                                      f"종가: {format(stock_df.iloc[i, 3],',')}, 거래량: {format(stock_df.iloc[i, 4],',')}")
    return ConversationHandler.END

def cancel(update, context):
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def telegram_connection():
    logger.info(f"activate telegram connection")
    updater = Updater("1941923189:AAEmoXlilPt2PpK2qXPH8-3Ya2bVH880ZXs", use_context=True)
     # define updater
    updater.dispatcher.add_handler(CommandHandler('kbdon', f_keyboarding))
    updater.dispatcher.add_handler(CommandHandler('kbdoff', f_unkeyboarding))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('stock', f_stock)],
        states={
            STOCK_NAME: [MessageHandler(Filters.text & ~Filters.command, stock_name)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    updater.dispatcher.add_handler(conv_handler)

    updater.dispatcher.add_handler(CommandHandler('news', f_news))
    updater.dispatcher.add_handler(CommandHandler('quit', f_quit))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, message_ctrl))
    # updater.dispatcher.add_handler(MessageHandler(Filters.text, message_ctrl))
    updater.start_polling()
    updater.idle()
    print(updater)

def main():
    telegram_connection()

if __name__ == '__main__':
    main()#