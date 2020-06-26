# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd

class MaoyanmoviesPipeline:
    def process_item(self, item, spider):
        name = item['name']
        category = item['category']
        date = item['date']
        movie_info = [[name, category, date]]
        df = pd.DataFrame(movie_info, columns=['电影名称', '电影类型', '上映时间'])
        df.to_csv('./movies.csv', mode='a', encoding='gbk', index=False, header=False)

        return item