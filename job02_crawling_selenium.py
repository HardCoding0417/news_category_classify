from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
from time import sleep
import datetime


option = webdriver.ChromeOptions()
user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")

option.add_argument('user-agent='+ user_agent)
option.add_argument('lang=ko_KR')
# option.add_argument('headless')
# option.add_argument('window-size=1920x1080')
# option.add_argument('disable=gpu')
# option.add_argument('--no sandbox')

# 최신버전 설정
service = ChromeService(executable_path = ChromeDriverManager().install())

# 크롬 드라이버 옛날 방식
# driver = webdriver.Chrome('./chromedriver', options=option)

# 크롬 드라이버 최신 방식
driver = webdriver.Chrome(service=service, )

category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']
pages = [110, 110, 110, 70, 110, 70]
df_titles = pd.DataFrame()

# 다중 for문은 내부부터 차근차근 만들자
for l in range(6):
    section_url = f'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{l}'
    titles = []
    for k in range(1,3):
        url = section_url + f'#&date=%2000:00:00&page={k}'
        driver.get(url)
        sleep(0.5)
        for i in range(1, 5):
            for j in range(1, 6):
                title = driver.find_element('xpath', '//*[@id="section_body"]/ul[{}]/li[{}]/dl/dt[2]/a'.format(i, j)).text
                title = re.compile('[^가-힣]').sub(' ', title)
                titles.append(title)
    df_section_title = pd.DataFrame(titles, columns= ['titles'])
    df_section_title['category'] = category[l]
    df_titles = pd.concat([df_titles, df_section_title], ignore_index=True)
df_titles.to_csv('./crawling_data/crawling_data.csv')

print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())



