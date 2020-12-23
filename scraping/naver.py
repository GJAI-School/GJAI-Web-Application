import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import re
import csv

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

for movie_select in load_soup(80):
    for data in movie_select:
        if data.select_one("td.title > .tit5 > a") is not None:
            movie_num = data.select_one("td.title > .tit5 > a")['href'].split('=')[1]
            movie_id.append(movie_num)

for movie_num in movie_id:
    base_url = f'https://movie.naver.com/movie/bi/mi/basic.nhn?code={movie_num}'
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    movie = soup.select_one('#content > .article')

    if movie is None:
        continue

    title = movie.select_one('div.mv_info_area > div.mv_info > h3').get_text()
    star = movie.select_one('div.mv_info_area > div.mv_info > div > div > a > div > span > span').get_text().split("평점")[1]

    genre = []
    for num in range(1, 10):
        if movie.select_one(f'div.mv_info_area > div.mv_info > dl > dd:nth-of-type(1) p > span:nth-of-type(1) > a:nth-of-type({num})') is not None:
            movie_genre = movie.select_one(f'div.mv_info_area > div.mv_info > dl > dd:nth-of-type(1) p > span:nth-of-type(1) > a:nth-of-type({num})').get_text()
            genre.append(movie_genre)
        else:
            break

    director = movie.select_one('div.mv_info_area > div.mv_info > dl > dd > p > a').get_text()

    summary = movie.select_one('div.section_group.section_group_frst > div:nth-of-type(1) > div > div.story_area > p').get_text()

    print(title, star, genre, director, summary)

    movie_data = {
        'title' : title,
        'star' : star,
        'genre' : genre,
        'director' : director,
        'summary' : summary
    }

    with open('./naver.csv', 'a', encoding='UTF8') as csvfile:
        fieldnames = ['title', 'star', 'genre', 'director', 'summary']
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writerow(movie_data)





