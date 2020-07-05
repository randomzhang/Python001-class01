# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql

dbInfo = {
    'host' : 'localhost',
    'port' : 3306,
    'user' : 'root',
    'password' : 'rootroot',
    'db' : 'test'
}

sqls = "insert into movies(name,type,time) values (%s,%s,%s)"

class ConnDB(object):
    def __init__(self, dbInfo, sqls):
        self.host = dbInfo['host']
        self.port = dbInfo['port']
        self.user = dbInfo['user']
        self.password = dbInfo['password']
        self.db = dbInfo['db']
        self.sqls = sqls

        # self.run()

    def run(self,data):
        conn = pymysql.connect(
            host = self.host,
            port = self.port,
            user = self.user,
            password = self.password,
            db = self.db
        )
        # 游标建立的时候就开启了一个隐形的事物
        cur = conn.cursor()
        #异常处理
        try:
            cur.execute(self.sqls,data)
            # 关闭游标
            cur.close()
            conn.commit()
        except:
            conn.rollback()
        # 关闭数据库连接
        conn.close()

class SpidersPipeline:
    def process_item(self, item, spider):

        # #把dict转换成dataframe，要先转成list
        # movie=[item]
        #
        # movie1 = pd.DataFrame(data=[item])
        # #mode='a'是代表追加数据，不覆盖
        # movie1.to_csv('./movie1.csv', encoding='utf8', index=False, mode='a', header=False)

        db = ConnDB(dbInfo, sqls)
        data = (item['name'],item['category'],item['date'])

        # 插入数据库-异常处理
        try:
            db.run(data)
        except Exception as e:
            print(e)

        return item
