import requests
from bs4 import BeautifulSoup
import csv

# 스크래핑하고 싶은 부분을 찾아서 패턴을 찾아본다. 
# 네이버뉴스 들고오기에서는 다음과 같이 start_num부분이 패턴이된다. 

def get_soup_object(search):
    soup_object = [] # soup객체들을 저장시킬 list

    # 웹페이지 패턴 확인. 검색이름과 페이지수 확인.
    for i in range(1, 102, 10): 
        base_url = f'https://search.naver.com/search.naver?&where=news&query={search}&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&cluster_rank=76&start='
        start_num = i
        end_url = '&refresh_start=0'

        # 다시 하나의 url로 합치기
        URL = base_url+str(start_num)+end_url

        # 요청보내기.
        # bs4를 통해서 html파싱
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        soup_object.append(soup)
    
    return soup_object


# 함수화를 일상화하자. 코드를 길게 짜는것은 상관없지만 효율적으로 짤수가 있다.
# 같은 곳에 있으면 상관없지만 다른곳에 있는경우 다시 request를 보내야 하는 경우가 생긴다.

# select은 결과값이 리스트형태로 저장이 된다. 나중에 여러개를 할 때 리스트형태로 들고와서 반복문을 사용하면 편하게 도출가능.
# select_one 리스트형태 x
# html의 구조를 파악하여 원하는 데이터가 있는 곳으로 이동한다.

# 반복문으로 배열 돌면서, 원하는데이터 출력하기.

search = input("원하시는 검색어를 입력하시오 :")
soup_object = get_soup_object(search)

for soup in soup_object:    
    news_select = soup.select('div[id=wrap] > div[id=container] > div[id=content] > div[id=main_pack] > div.news.mynews.section._prs_nws > ul > li')
    for news in news_select:
        href = news.select_one('dl > dt > a')['href']
        title = news.select_one('dl > dt > a')['title']

        news_data = {
            'title' : title,
            'link' : href
        }

        with open(f'{search}.csv', 'a', encoding='utf-8-sig') as csvfile:
            fieldnames = ['title', 'link']
            rbr = csv.DictWriter(csvfile, fieldnames=fieldnames)
            rbr.writerow(news_data)