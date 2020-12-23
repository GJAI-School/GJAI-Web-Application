# 더 쉽게 복사해서 하는등의 방법이 있지만, 기본 구조를 이해하기 위해서 하나씩 차근차근 진행해보았습니다 !
# 다른 여러 방법으로 해보셔도 좋아요 :)

import requests
from bs4 import BeautifulSoup

base_url = 'https://search.naver.com/search.naver?&where=news&query=%EA%B4%91%EC%A3%BC%EC%9D%B8%EA%B3%B5%EC%A7%80%EB%8A%A5%EC%82%AC%EA%B4%80%ED%95%99%EA%B5%90&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&cluster_rank=69&start='
start_num = 1
end_url = '&refresh_start=0'

URL = base_url + str(start_num) + end_url

response = requests.get(URL)
soup = BeautifulSoup(response.text, 'html.parser')

news_section = soup.select(
    'div[id=wrap] > div[id=container] > div[id=content] > div[id=main_pack] > div.news.mynews.section._prs_nws > ul[class=type01] > li')


for news in news_section:
    a_tag = news.select_one('dl > dt > a')
    news_title = a_tag['title']
    news_link = a_tag['href']
    print(news_title)
    print(news_link, '\n')
