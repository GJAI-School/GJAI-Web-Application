import requests
from bs4 import BeautifulSoup
import re

# 11024
# https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200825
# https://movie.naver.com/movie/bi/mi/basic.nhn?code=10200

# # 청소년 불가 영화 code
# base_url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.nhn?grade=1001004'
# option = '&page='
# tail = 1

# remove_list = []
# for tail in range(tail, 768, 1):
#     URL = base_url + option + str(tail)

#     response = requests.get(URL)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     remove = soup.select('#content > .article > div:nth-of-type(1) > #cbody > #old_content > ul > li')
    
#     for re in remove:
#         remove = re.select_one('a')['href'].split('code=')[1]
#         remove_list.append(remove)

# print(remove_list)
# print(len(remove_list))



def load_soup(num):
    soup_object = []

    for i in range(num):
        base_url = f"https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200825&tg=0&page={i}"
        response = requests.get(base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        data_select = soup.select("#old_content > table > tbody > tr")
        soup_object.append(data_select)

    return soup_object


movie_id = []

for movie_select in load_soup(1):
    for data in movie_select:
        if data.select_one("td.title > div.tit5 > a") is not None:
            movie_num = data.select_one("td.title > div.tit5 > a")['href'].split('=')[1]
            movie_id.append(movie_num)

# 크롤링 메인부분
base_url = 'https://movie.naver.com/movie/bi/mi/basic.nhn'
option = '?code='
code = 171538 # 19999까지 11000

for code in range(code, 171540, 1):

    URL = base_url + option + str(code)
    response = requests.get(URL)

    code = str(code)
    # 청소년 불가 영화 예외처리

    soup = BeautifulSoup(response.text, 'html.parser')
    movie = soup.select_one(
        '#content > .article')

    if movie is None:
        continue

    if movie.select_one('.mv_info_area > .mv_info > .info_spec > dd:nth-of-type(4)'):
        remove = movie.select_one('.mv_info_area > .mv_info > .info_spec > dd:nth-of-type(4) > p > a')
        remove = remove.text
        # print(code-11000, remove)

    a_tag = movie.select_one('.mv_info_area > .mv_info > .h_movie > a')
    movie_title = a_tag.text

    a_tag2 = movie.select('.mv_info_area > .mv_info > .info_spec > dd > p > span:nth-of-type(1) > a')

    # remove = movie.select_one('.mv_info_area > .mv_info > .info_spec > dd:nth-of-type(4)')

    movie_genre = []
    for genre in a_tag2:
        movie_genre.append(genre.text)

    summary = movie.select('div:nth-of-type(4) > .obj_section > .video > .story_area > p')

    print('id:', int(code)-12000, 'title:', movie_title, ' genre:',movie_genre)
    print('summary:', summary ,'\n')
