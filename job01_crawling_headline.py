from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import datetime
from time import sleep

category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']
url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100'
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}

df_titles = pd.DataFrame()
re_title = re.compile('[^가-힣]|a-z|A-Z')

for i in range(6):
    response = requests.get('https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(i), headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    title_tags = soup.select('.sh_text_headline')
    titles = []
    for title_tag in title_tags:
        titles.append(re.compile('[^가-힣]|a-z|A-Z').sub(' ', title_tag.text))
    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    df_section_titles['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_titles], axis='rows')

print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())
df_titles.to_csv('./crawling_data/naver_headline_news_{}.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d')), index=False)

# response = requests.get(url, headers=headers)
# # print(list(response))
# # print(type(response))

# # print(soup)

# title_tags = soup.select('.sh_text_headline')
# print(title_tags)
# print(len(title_tags))
# print(type(title_tags[0]))
#
# titles = []
# for title_tag in title_tags:
#     titles.append(re.compile('[^가-힣|a-z|A-Z|\u4E00-\u9FFF|,.\'"]').sub(' ', title_tag.text))
# print(titles)
# print(len(titles))
#
# # 뉴스 URL
# # https://news.naver.com/
# # 정치탭 URL
# # https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100
# # 정치 헤드라인의 형식
# # <a href="https://n.news.naver.com/mnews/article/032/0003253663?sid=100"
#
# # class="sh_text_headline nclicks(cls_pol.clsart)">강서구청장 보궐선거 결과가 가져올 여권의 ‘다른 미래’</a>
#
