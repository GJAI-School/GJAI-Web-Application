import requests
from bs4 import BeautifulSoup, NavigableString, Tag

page_dic = {'1990': 17, '1991' : 16, '1992' : 20, '1993': 21, '1994' : 19, '1995' : 17, '1996' : 17, '1997' : 17, '1998' : 15, '1999' : 16, 
            '2000' : 19, '2001' : 17, '2002' : 18, '2003' : 20, '2004' : 38, '2005' : 21, '2006' : 24, '2007' : 26, '2008' : 28, '2009' : 24,
            '2010' : 29, '2011' : 41, '2012' : 44, '2013' : 61, '2014' : 76, '2015' : 71, '2016' : 59, '2017' : 53, '2018' : 50, '2019' : 43,
            '2020' : 30}

def load_soup(dic):
    years = list(dic.keys())
    pages = list(dic.values())

    soup_object = []
    for idx, year in enumerate(years): 
        for page in range(1, pages[idx]+1):
            # print(year ,page)
            base_url = f"https://movie.naver.com/movie/sdb/browsing/bmovie.nhn?open={year}&page={str(page)}"
            response = requests.get(base_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            data_select = soup.select("#old_content > ul > li")
            soup_object.append(data_select)
    return soup_object

def load_movie_id(dic):
    movie_id = []

    for movie_select in load_soup(dic):
        # print(movie_select)
        for data in movie_select:
            movie_id.append(data.select_one('a')['href'].split('=')[1])
    return movie_id

def load_url(subject, movie_num):
    base_url = f'https://movie.naver.com/movie/bi/mi/{subject}.nhn?code={movie_num}'
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    article = soup.select_one('#content > div.article')
    return article



