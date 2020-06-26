# -*- coding: utf-8 -*-
import scrapy
from maoyanmovies.items import MaoyanmoviesItem
from scrapy.selector import Selector
from http.cookies import SimpleCookie

class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']
    cookies_fromchrome = '__mta=44347931.1593097833341.1593098568161.1593168851120.5; uuid_n_v=v1; uuid=02FBD510B6F611EAB11C23537EB4C64BBD09CCAD5A644B4CBE341FE3E99A9F12; _lxsdk_cuid=172ec07cabfb-0cb34f5e9c7f0e-4353760-e1000-172ec07cac0c8; _lxsdk=02FBD510B6F611EAB11C23537EB4C64BBD09CCAD5A644B4CBE341FE3E99A9F12; mojo-uuid=8de9de8c3eb999dc880c598ad9350875; _csrf=d2ca363caede1a5436f7bf248add6f6346ba9a2196d9f65edb6e785e8b143dd0; mojo-session-id={"id":"55ba3538e31e5485feb0a50fce83228d","time":1593168816648}; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1593097833,1593168817; __mta=44347931.1593097833341.1593098568161.1593168816846.5; mojo-trace-id=3; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593168851; _lxsdk_s=172f042eaa2-4c8-6de-35e%7C%7C4'
    cookie = SimpleCookie(cookies_fromchrome)
    cookies = {i.key: i.value for i in cookie.values()}
    # def parse(self, response):
    #     pass

    def start_requests(self):
        url = 'https://maoyan.com/films?showType=3'
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=False, cookies=self.cookies)

    # 解析函数
    def parse(self, response):
        # 打印网页的url
        # print(response.url)
        # 打印网页的内容
        # print(response.text)

        # soup = BeautifulSoup(response.text, 'html.parser')
        # title_list = soup.find_all('div', attrs={'class': 'hd'})
        movies = Selector(response=response).xpath('//div[@class="movie-item film-channel"]')
        i = 0
        for movie in movies:
        #     title = i.find('a').find('span',).text
        #     link = i.find('a').get('href')
            # 路径使用 / .  .. 不同的含义　
            if i == 10:
                break
            i += 1
            link = movie.xpath('./a/@href')
            # print("https://maoyao.com"+link.extract_first())
            yield scrapy.Request(url='https://maoyan.com'+link.extract_first().strip(),
                                 callback=self.parse2,
                                 )

    def parse2(self, response):
        item = MaoyanmoviesItem()
        movies = Selector(response=response).xpath('//div[@class="movie-brief-container"]')
        print(movies)
        for movie in movies:
            item['name'] = movie.xpath('./h1/text()').extract_first()
            item['category'] = movie.xpath('./ul/li/a/text()').extract()
            item['date'] = movie.xpath('./ul/li[last()]/text()').extract_first().strip()
        yield item



