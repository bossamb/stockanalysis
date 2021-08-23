import pandas_datareader.data as pdweb
from pandas_datareader import data as pdr
# import yfinance # must pip install first
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from selenium import webdriver

def get_stock_data(name, start_date, end_date=datetime.today().strftime('%Y-%m-%d')):
    data = pdr.get_data_yahoo(name, start_date, end_date)
    # print(data)
    # plt.plot(data['Close'])
    # plt.plot(data['Volume'], secondary)
    # plt.show()
    return data

def get_stock_name():
    count = 0
    while count <= 3:
        try:
            stock_name = input("Enter the stock you want to search: ")
            options = webdriver.ChromeOptions()
            options.add_argument("headless")
            URL = 'https://www.naver.com/'
            driver = webdriver.Chrome(executable_path='//chromedriver', options=options)
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
            break
        except:
            count += 1
        if count == 3:
            print('검색에 실패했습니다.')
            return None
            break

# # Connecting server
# received = getLevel(driver)
# for d in received:
#     print(d.text)
# print(getLevel(driver))

if __name__=='__main__':
    stock_info = get_stock_name()
    if len(stock_info) != 0:
        print(stock_info)
    name = stock_info[1]
    start_date = input('Enter the start date(YYYY-MM-DD): ')
    # start_date = '2017-05-20'
    data = get_stock_data(name, start_date)
    print(data.columns)
    sns.lineplot(x=data.index, y=data['Close'])
    ax2 = plt.twinx()
    plt.xticks(rotation=30)
    plt.show()