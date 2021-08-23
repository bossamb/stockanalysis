from selenium import webdriver

def getLevel(driver):
    search_box = driver.find_elements_by_xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/span[2]')
    return search_box




def main():
    URL = 'https://finance.yahoo.com/quote/%5EKS11?p=%5EKS11'
    driver = webdriver.Chrome(executable_path='/Users/yh/Pycharm/CrawlingLostArk/chromedriver')
    driver.get(url=URL)
    driver.find_element_by_xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/span[2]')
    # Connecting server
    received = getLevel(driver)
    for d in received:
        print(d.text)
    print(getLevel(driver))

if __name__ == "__main__":
    main()
