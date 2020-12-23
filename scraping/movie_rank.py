import requests
from bs4 import BeautifulSoup
import csv

response = requests.get('https://movie.naver.com/movie/running/current.nhn')
soup = BeautifulSoup(response.text, 'html.parser')


select_movie = soup.select('div[id=wrap] > div[id=container] > div[id=content] > div.article > div.obj_section > div.lst_wrap > ul > li')
# print(select_movie)


for movie in select_movie:
    title = movie.select_one('dl > dt > a').get_text()
    code = movie.select_one('dl > dt > a')['href'].split('=')[1]
    
    movie_data = {
        'code' : code, 
        'title' : title
        }

    with open('movie_rank.csv', 'a', encoding='utf-8-sig') as csvfile:
            fieldnames = ['code', 'title']
            rbr = csv.DictWriter(csvfile, fieldnames=fieldnames)
            rbr.writerow(movie_data)

   