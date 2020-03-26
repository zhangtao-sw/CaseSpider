# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import redis
import pymysql
from .settings import *
from hashlib import md5

class CasesystemPipeline(object):
    def process_item(self, item, spider):
        print(item)
        return item

class MysqlPipeline(object):
    def open_spider(self,spider):
        self.db = pymysql.connect(
            MYSQL_HOST,MYSQL_USER,MYSQL_PWD,MYSQL_DB,
            charset=MYSQL_CHAR
        )
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        print(item)

        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.db.close()

class RedisPipeline(object):
    def open_spider(self,spider):
        self.r = redis.Redis(host=REDIS_HOST,port=REDIS_PORT,db=REDIS_DB)
    def process_item(self, item, spider):
        url=item["Case_link"]
        url_md5=md5(url.encode()).hexdigest()
        self.r.sadd("url",url_md5)
        print("%s 写入redis成功"%url)
        return item

    def close_spider(self,spider):
        pass


