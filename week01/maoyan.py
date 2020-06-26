# 使用BeautifulSoup解析网页

import requests
from bs4 import BeautifulSoup as bs
# bs4是第三方库需要使用pip命令安装


user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'

header = {'user-agent':user_agent,
          'Cookie': '__mta=44347931.1593097833341.1593098568161.1593168851120.5; uuid_n_v=v1; uuid=02FBD510B6F611EAB11C23537EB4C64BBD09CCAD5A644B4CBE341FE3E99A9F12; _lxsdk_cuid=172ec07cabfb-0cb34f5e9c7f0e-4353760-e1000-172ec07cac0c8; _lxsdk=02FBD510B6F611EAB11C23537EB4C64BBD09CCAD5A644B4CBE341FE3E99A9F12; mojo-uuid=8de9de8c3eb999dc880c598ad9350875; _csrf=d2ca363caede1a5436f7bf248add6f6346ba9a2196d9f65edb6e785e8b143dd0; mojo-session-id={"id":"55ba3538e31e5485feb0a50fce83228d","time":1593168816648}; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1593097833,1593168817; __mta=44347931.1593097833341.1593098568161.1593168816846.5; mojo-trace-id=3; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593168851; _lxsdk_s=172f042eaa2-4c8-6de-35e%7C%7C4'}

myurl = 'https://maoyan.com/films?showType=3'
base_url = 'https://maoyan.com'
response = requests.get(myurl,headers=header)
bs_info = bs(response.text, 'html.parser')

# 获取前十大电影url
url_list = []
for tags in bs_info.find_all('div', attrs={'class': 'movie-item film-channel'}):
    for atag in tags.find_all('a',):
        url_list.append(atag.get('href'))
        break
    if len(url_list) == 10:
        break

name_list = []
type_list = []
ondate_list = []
# 根据url获取电影名称、电影类型和上映时间
url_movie = [base_url + url for url in url_list]
for url in url_movie:
    response = requests.get(url, headers=header)
    bs_info = bs(response.text, 'html.parser')
    for tags in bs_info.find_all('div', attrs={'class': 'movie-brief-container'}):
        name_list.append(tags.find('h1').text)
        type_list_temp = []
        for atag in tags.find_all('a'):
            type_list_temp.append(atag.text)
        type_list.append(type_list_temp)
        for ltag in tags.find_all('li'):
            pass
        if ltag:
            ondate_list.append(ltag.text)
print(name_list)
print(type_list)
print(ondate_list)

import pandas as pd

movie1 = pd.DataFrame(columns=['电影名称', '电影类型', '上映时间'])
movie1['电影名称'] = name_list
movie1['电影类型'] = type_list
movie1['上映时间'] = ondate_list
# windows需要使用gbk字符集
movie1.to_csv('./movie1.csv', encoding='gbk', index=False)



