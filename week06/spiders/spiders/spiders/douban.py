# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from spiders.items import SpidersItem

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['http://douban.com/']

    def parse(self, response):
        pass

    def start_requests(self):
        url = f'https://movie.douban.com/top250?start=0'
        yield scrapy.Request(url=url, callback=self.parse, dont_filter=False)

    def parse(self, response):
        movies = Selector(response=response).xpath('//div[@class="hd"]')
        for movie in movies:
            item = SpidersItem()
            title = movie.xpath('./a/span/text()').extract_first()
            item['title'] = title
            link = movie.xpath('./a/@href').extract_first() + '/comments?status=P'
            yield scrapy.Request(url=link, meta={'item': item}, callback=self.parse2)

    def parse2(self, response):
        item = response.meta['item']
        item['comment'] = []
        comments = Selector(response=response).xpath('//div[@class="comment"]')
        for comment in comments:
            stars = comment.xpath(
                './h3/span[@class="comment-info"]/span[contains(@class, '
                '"rating")]/@class').extract_first()
            text = comment.xpath('./p/span[@class="short"]/text()').extract_first()
            item['comment'].append({'stars': stars, 'text': text})
        yield item