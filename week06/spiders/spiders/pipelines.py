# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import orator
from spiders.models import Movie
from spiders.models import Comment


class SpidersPipeline:
    def __init__(self, db_config):
        self.db_config = db_config

    @classmethod
    def from_crawler(cls, crawler):
        config = {
            'mysql': {
                'driver': 'mysql',
                'host': crawler.settings.get('MYSQL_HOST'),
                'database': crawler.settings.get('MYSQL_DB'),
                'user': crawler.settings.get('MYSQL_USER'),
                'password': crawler.settings.get('MYSQL_PASSWORD'),
            }
        }
        return cls(
            db_config=config
        )

    def open_spider(self, spider):
        db = orator.DatabaseManager(self.db_config)
        orator.Model.set_connection_resolver(db)

    def process_item(self, item, spider):
        movie = Movie.where('title', '=', item['title']).get().first()
        if movie is None:
            movie = Movie()
            movie.title = item['title']
            movie.save()

        for comment in item['comment']:
            db_comment = Comment()
            db_comment.movie_id = movie.id
            try:
                db_comment.stars = int(
                    comment['stars'].replace('allstar', '').replace('rating', ''))
            except Exception as err:
                print(err)
            db_comment.txt = comment['text']
            db_comment.save()

        return item