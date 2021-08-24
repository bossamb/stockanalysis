import telegram
import schedule
import time
from bs4 import BeautifulSoup as bs
import requests
import datetime

def job():
    now = time.localtime()
    telegram_sending(get_headlines())
    print("current time = ", str(now))

def telegram_sending(stuffs):
    token = "1941923189:AAEmoXlilPt2PpK2qXPH8-3Ya2bVH880ZXs"
    bot = telegram.Bot(token=token)
    chat_id = "1777070088"
    text = stuffs
    bot.sendMessage(chat_id=chat_id, text=text)

def get_headlines():
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

def main():
    schedule.every().hours.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
