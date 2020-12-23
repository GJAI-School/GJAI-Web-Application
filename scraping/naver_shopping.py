import requests
from bs4 import BeautifulSoup
import json

headers = {
    'authority': 'search.shopping.naver.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Mobile Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://search.shopping.naver.com/search/all?frm=NVSHATC&origQuery=%EB%85%B8%ED%8A%B8%EB%B6%81&pagingIndex=2&pagingSize=40&productSet=total&query=%EB%85%B8%ED%8A%B8%EB%B6%81&sort=rel&timestamp=&viewType=list',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': 'NNB=Z67XSK2MUIAF6; NRTK=ag#20s_gr#0_ma#-2_si#-2_en#-2_sp#-2; MM_NEW=1; NFS=2; MM_NOW_COACH=1; m_loc=956d8c2606a311274f353f3251f213bd9d0f2c4eefa64476fbf43fb73bee8e19; AD_SHP_BID=21; _fbp=fb.1.1596526001595.1709757470; _ga=GA1.1.154328998.1594890250; _ga_4BKHBFKFK0=GS1.1.1596526001.1.1.1596526003.58; nx_ssl=2; page_uid=UzuWVdprvTVssMx10VRssssssLs-463000; BMR=s=1597047699644&r=https%3A%2F%2Fm.blog.naver.com%2Fsamsjang%2F220979751089&r2=https%3A%2F%2Fwww.google.com%2F; JSESSIONID=7B554E1467F7AEB041AB5444367305A9; spage_uid=UzuWVdprvTVssMx10VRssssssLs-463000',
}

params = (
    ('origQuery', '\uB178\uD2B8\uBD81'),
    ('pagingIndex', '2'),
    ('pagingSize', '40'),
    ('productSet', 'total'),
    ('query', '\uB178\uD2B8\uBD81'),
    ('sort', 'rel'),
    ('timestamp', ''),
    ('viewType', 'list'),
)

response = requests.get('https://search.shopping.naver.com/search/all', headers=headers, params=params)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://search.shopping.naver.com/search/all?origQuery=%EB%85%B8%ED%8A%B8%EB%B6%81&pagingIndex=2&pagingSize=40&productSet=total&query=%EB%85%B8%ED%8A%B8%EB%B6%81&sort=rel&timestamp=&viewType=list', headers=headers)

# print(response.text)
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)

# select_list = soup.select('#__next > div > div.container > div.style_inner__18zZX > div.style_content_wrap__1PzEo > div.style_content__2T20F > ul > div > div:nth-child(1) > li > div > div.basicList_info_area__17Xyo > div.basicList_desc__2-tko > div.basicList_detail_box__3ta3h')
