import requests
from bs4 import BeautifulSoup
import csv

response = requests.get('https://movie.naver.com/movie/running/current.nhn')
soup = BeautifulSoup(response.text, 'html.parser')


select_movie = soup.select('div[id=wrap] > div[id=container] > div[id=content] > div.article > div.obj_section > div.lst_wrap > ul > li')
# print(select_movie)


movie_lst = []
for movie in select_movie:
    title = movie.select_one('dl > dt > a').get_text()
    code = movie.select_one('dl > dt > a')['href'].split('=')[1]
    
    movie_data = {
        'code' : code, 
        'title' : title
        }
    movie_lst.append(movie_data)
    # save_csv
    # with open('movie_rank.csv', 'a', encoding='utf-8-sig') as csvfile:
    #         fieldnames = ['code', 'title']
    #         rbr = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #         rbr.writerow(movie_data)

for movie_info in movie_lst:
    movie_code = movie_info['code']

    headers = {
        'authority': 'movie.naver.com',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Mobile Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'iframe',
        'referer': 'https://movie.naver.com/movie/bi/mi/point.nhn?code=189069',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'NNB=Z67XSK2MUIAF6; NRTK=ag#20s_gr#0_ma#-2_si#-2_en#-2_sp#-2; MM_NEW=1; NFS=2; MM_NOW_COACH=1; m_loc=956d8c2606a311274f353f3251f213bd9d0f2c4eefa64476fbf43fb73bee8e19; _fbp=fb.1.1596526001595.1709757470; _ga=GA1.1.154328998.1594890250; _ga_4BKHBFKFK0=GS1.1.1596526001.1.1.1596526003.58; NM_THUMB_PROMOTION_BLOCK=Y; nx_ssl=2; page_uid=UyW2cdp0Jy0ssUMiQ9ossssss9G-266470; csrf_token=2be5eb53-28ba-498f-95ca-2e5c865b984e',
    }

    params = (
        ('code', movie_code),
        ('type', 'after'),
        ('isActualPointWriteExecute', 'false'),
        ('isMileageSubscriptionAlready', 'false'),
        ('isMileageSubscriptionReject', 'false'),
    )

    response = requests.get('https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn', headers=headers, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    review_info = soup.select('body > div > div > div.score_result > ul > li')

    for num, info in enumerate(review_info):
        star = info.select_one('div.star_score > em').get_text() 

        if info.select_one(f'div.score_reple > p > span#_filtered_ment_{num} > span#_unfold_ment{num}') is None:
            reple = info.select_one(f'div.score_reple > p > span#_filtered_ment_{num}').get_text().strip()
        elif info.select_one(f'div.score_reple > p > span#_filtered_ment_{num} > span#_unfold_ment{num}'):
            reple = info.select_one(f'div.score_reple > p > span#_filtered_ment_{num} > span#_unfold_ment{num} > a')['data-src']
        
        print(star, reple)
        break