import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import csv
import re

def load_soup(num):
    soup_object = []

    for i in range(1, num+1):
        base_url = f"https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200825&tg=0&page={i}"
        response = requests.get(base_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        data_select = soup.select("#old_content > table > tbody > tr")
        soup_object.append(data_select)
    return soup_object

def load_url(subject, movie_num):
    base_url = f'https://movie.naver.com/movie/bi/mi/{subject}.nhn?code={movie_num}'
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    article = soup.select_one('#content > div.article')

    return article


def load_movie_id(page_num):
    movie_id = []

    for movie_select in load_soup(page_num):
        for data in movie_select:
            if data.select_one("td.title > div.tit5 > a") is not None:
                movie_num = data.select_one("td.title > div.tit5 > a")['href'].split('=')[1]
                movie_id.append(movie_num)

    return movie_id

# 영화 아이디 불러오기
movie_id = load_movie_id(1)
# print(movie_id)
# print(len(movie_id))


for idx, movie_num in enumerate(movie_id):
    # print(idx+1)
    basic_article = load_url('basic', movie_num) # 줄거리를 보여주는 페이지
    datail_article = load_url('detail', movie_num) # 출연배우를 보여주는 페이지

    # 19 청불영화에 대한 예외처리
    if basic_article is None:
        continue
    
    # 제목 
    title = basic_article.select_one('div.mv_info_area > div.mv_info > h3').get_text().replace('\n', '')
    # print(title)

    # 네티즌 점수 
    star_lst = []
    for num in range(1,5):
        star = basic_article.select_one(f'div.mv_info_area > div.mv_info > div.main_score > div.score.score_left > div.star_score > a > em:nth-of-type({num})').get_text()
        star_lst.append(str(star))
    # print("".join(i for i in star_lst))

    # 장르
    genre_lst = []
    a = basic_article.select(f'div.mv_info_area > div.mv_info > dl')
    for i in a:
        print(i.select_one('dt')['class'])

    if basic_article.select_one(f'div.mv_info_area > div.mv_info > dl > dt.step1 > em').get_text() != "개요()":
        genre = ""
    else:
        for num in range(1, 5):
            if basic_article.select_one(f'div.mv_info_area > div.mv_info > dl > dd:nth-of-type(1) p > span:nth-of-type(1) > a:nth-of-type({num})') is not None: 
                genre = basic_article.select_one(f'div.mv_info_area > div.mv_info > dl > dd:nth-of-type(1) p > span:nth-of-type(1) > a:nth-of-type({num})').get_text()
                genre_lst.append(genre)
            else:
                break
        
    # print((', ').join(i for i in genre_lst))
    
    # 줄거리
    #content > div.article > div.section_group.section_group_frst > div:nth-of-type(1) > div > div > div > h4
    if basic_article.select_one('div.section_group.section_group_frst > div:nth-of-type(1) > div > div > div > h4').get_text() != "줄거리":
        summary = ""
    else:
        summary = basic_article.select_one('div.section_group.section_group_frst > div:nth-of-type(1) > div > div.story_area > p').get_text().replace('\r', "").replace('\xa0', "")
    # print(summary)

    # 영화 감독
    if basic_article.select_one('div.mv_info_area > div.mv_info > dl > dt.step2 > em').get_text() != "감독":
        movie_director = ""
    else:
        movie_director = basic_article.select_one('div.mv_info_area > div.mv_info > dl > dd:nth-of-type(2) > p > a').get_text()
    # print(movie_director)

    # 영화 등급
    #content > div.article > div.mv_info_area > div.mv_info > dl > dt.step4 > em
    if basic_article.select_one('div.mv_info_area > div.mv_info > dl > dt.step4 > em').get_text() != "등급":
        movie_rating = ""
    else:
        movie_rating_count = len(basic_article.select_one('div.mv_info_area > div.mv_info > dl > dd'))
        # print(movie_rating_count)
        # movie_rating = basic_article.select_one('div.mv_info_area > div.mv_info > dl > dd:nth-of-type(4) > p > a').get_text()
        


    #     movie_rating = basic_article.select_one('div.mv_info_area > div.mv_info > dl > dd:nth-of-type(4) > p > a').get_text()
    # elif basic_article.select_one('div.mv_info_area > div.mv_info > dl > dd:nth-of-type(4) > p > a') is None:
    #     movie_rating = basic_article.select_one('div.mv_info_area > div.mv_info > dl > dd:nth-of-type(3) > p > a').get_text()
    # elif basic_article.select_one('div.mv_info_area > div.mv_info > dl > dd:nth-of-type(3) > p > a') is None:
    #     movie_rating = basic_article.select_one('div.mv_info_area > div.mv_info > dl > dd:nth-of-type(2) > p > a').get_text()
    # elif basic_article.select_one('div.mv_info_area > div.mv_info > dl > dd:nth-of-type(2) > p > a') is None:
    #     movie_rating = basic_article.select_one('div.mv_info_area > div.mv_info > dl > dd:nth-of-type(1) > p > a').get_text()
    # else:
    #     movie_rating = ""
    # print(movie_rating)


    # 영화배우
    #content > div.article > div.section_group.section_group_frst > div.obj_section.noline > div > div.lst_people_area.height100
    movie_actors = datail_article.select('div.section_group.section_group_frst > div.obj_section.noline > div > div.lst_people_area.height100')
    actor_lst = []

    # 영화배우 count
    actor_counts = datail_article.select('div.section_group.section_group_frst > div.obj_section.noline > div > div.lst_people_area.height100 > ul > li')
    actor_counts = len(actor_counts)

    for actors in movie_actors:
        for num in range(1, actor_counts+1):
            if actors.select_one(f'ul > li:nth-of-type({num}) > div > div > p.in_prt > em').get_text() == '주연':
                if actors.select_one(f'ul > li:nth-of-type({num}) > div > a') is not None:
                    actor = actors.select_one(f'ul > li:nth-of-type({num}) > div > a').get_text()
                    actor_lst.append(actor)
                elif actors.select_one(f'ul > li:nth-of-type({num}) > div > span') is not None:
                    actor = actors.select_one(f'ul > li:nth-of-type({num}) > div > span').get_text()
                    actor_lst.append(actor)
            else:
                break
    # print(actor_lst)

    
    # movie_data = {
    #     'movie_id' : movie_num,
    #     'title' : title,
    #     'star' : "".join(i for i in star_lst),
    #     'movie_rating' : movie_rating,
    #     'genre' : genre_lst,
    #     'director' : movie_director,
    #     'actors' : actor_lst,
    #     'summary' : summary
    # }

    # print(movie_data, '\n')

    # with open('./movie_data3.csv', 'a', encoding='utf-8') as csvfile:
    #     fieldnames = ['movie_id', 'title', 'star', 'movie_rating',  'genre', 'director', 'actors', 'summary']
    #     csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #     csvwriter.writerow(movie_data)