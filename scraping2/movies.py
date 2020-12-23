import requests
from bs4 import BeautifulSoup

response = requests.get('https://movie.naver.com/movie/running/current.nhn')
soup = BeautifulSoup(response.text, 'html.parser')

movies_list = soup.select(
    '#content > .article > .obj_section > .lst_wrap > ul > li')

final_movie_data = []

for movie in movies_list:
    a_tag = movie.select_one('dl > dt > a')

    movie_title = a_tag.contents[0]
    movie_code = a_tag['href'].split('code=')[1]

    movie_data = {
        'title': movie_title,
        'code': movie_code
    }

    final_movie_data.append(movie_data)

for movie in final_movie_data:
    movie_code = movie['code']

    # 영화 리뷰의 경우 headers 체크를 따로 하지 않아서 굳이 보낼 필요 없음
    params = (
        ('code', movie_code),
        ('type', 'after'),
        ('isActualPointWriteExecute', 'false'),
        ('isMileageSubscriptionAlready', 'false'),
        ('isMileageSubscriptionReject', 'false'),
    )

    response = requests.get(
        'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn', params=params)

    soup = BeautifulSoup(response.text, 'html.parser')

    review_list = soup.select('body > div > div > div.score_result > ul > li')

    count = 0

    for review in review_list:
        score = review.select_one('div.star_score > em').text
        reple = ''

        # 일반적인 경우 먼저 처리 (일반적인 것을 먼저 처리하는 것이 효율적이다)
        if review.select_one(f'div.score_reple > p > span#_filtered_ment_{count} > span#_unfold_ment{count}') is None:
            reple = review.select_one(
                f'div.score_reple > p > span#_filtered_ment_{count}').text.strip()
        # 리뷰가 긴 경우 처리
        elif review.select_one(f'div.score_reple > p > span#_filtered_ment_{count} > span#_unfold_ment{count}'):
            reple = review.select_one(
                f'div.score_reple > p > span#_filtered_ment_{count} > span > a')['data-src']

        print(score, reple)

        count += 1
