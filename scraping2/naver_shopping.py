import requests
from bs4 import BeautifulSoup

import json


headers = {
    'authority': 'search.shopping.naver.com',
    'accept': 'application/json, text/plain, */*',
    'urlprefix': '/api',
    'logic': 'PART',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://search.shopping.naver.com/search/all?query=%EB%85%B8%ED%8A%B8&frm=NVSHATC&prevQuery=%EB%85%B8%ED%8A%B8',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': 'NNB=2UQUKRQQX2TV4; NDARK=N; NRTK=ag#10s_gr#4_ma#2_si#-2_en#-2_sp#-2; nx_ssl=2; MM_NEW=1; NFS=2; MM_NOW_COACH=1; nid_inf=-1605587342; NID_JKL=UWAeiCgMnd2dy/jvWgdajmJpxM70PJcBVLX2E5Hoo7k=; AD_SHP_BID=22; ASID=798a875500000173896aea1300000058; JSESSIONID=3E7F6F22FB222F281315156F40B09AFF; BMR=s=1595751446748&r=https%3A%2F%2Fm.blog.naver.com%2FPostView.nhn%3FblogId%3Dinajjang97%26logNo%3D221612522577%26categoryNo%3D39%26proxyReferer%3Dhttps%3A%252F%252Fwww.google.com%252F&r2=https%3A%2F%2Fwww.google.com%2F; page_uid=Ux1YZsprvmZssmnd4LRssssss/Z-207281; _naver_usersession_=Jel78BkBLEjULXFqmGRQSQ==; spage_uid=Ux1YZsprvmZssmnd4LRssssss%2FZ-207281',
}

params = (
    ('sort', 'rel'),
    ('pagingIndex', '1'),
    ('pagingSize', '80'),
    ('viewType', 'list'),
    ('productSet', 'total'),
    ('frm', 'NVSHATC'),
    ('query', '노트'),
    ('origQuery', '노트'),
)

response = requests.get(
    'https://search.shopping.naver.com/search/all', headers=headers, params=params)

result_dict = json.loads(response.text)
print(result_dict)

with open('data.json', 'w', encoding='UTF-8') as outfile:
    json.dump(result_dict, outfile, ensure_ascii=False)
