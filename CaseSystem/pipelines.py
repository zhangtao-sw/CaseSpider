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
        return item


class Mysql_Pipeline(object):
    def open_spider(self, spider):
        self.db = pymysql.connect(
            MYSQL_HOST, MYSQL_USER, MYSQL_PWD, MYSQL_DB,
            charset=MYSQL_CHAR
        )
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        self.write_base_info(item)
        self.write_attachments(item)
        self.write_comments(item)
        self.write_kba_doc(item)
        return item

    def write_base_info(self, item):
        sql='insert into base_info(Case_Number,Case_link,Account_Name,Open_Time,Case_Owner,Contact_Name,Country,Subject,Description,PA1,PA2,PA3,OS_Android,Software_Product,Resolution_Summary,ResponsivenessToTheCase,QualityOfTechnicalSupport,ProfessionalismOfQCEngineer) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        L = [
            item['Case_Number'],item['Case_link'],item['Account_Name'],
            item['Open_Time'], item['Case_Owner'], item['Contact_Name'],
            item['Country'], item['Subject'], item['Description'],
            item['PA1'], item['PA2'], item['PA3'],
            item['OS_Android'], item['Software_Product'], item['Resolution_Summary'],
            item['ResponsivenessToTheCase'], item['QualityOfTechnicalSupport'], item['ProfessionalismOfQCEngineer']
        ]
        self.cursor.execute(sql,L)
        self.db.commit()

    def write_attachments(self, item):
        sql = 'insert into Attachments values(%s,%s,%s,%s,%s,%s,%s)'
        Case_Attachments=item['Case_Attachments']
        if not Case_Attachments:
            return
        L=[]
        for i in Case_Attachments:
            L.append((item['Case_Number'],i['link'],i['name'],i['Description'],i['type'],i['uploader'],i['size']))
        self.cursor.executemany(sql, L)
        self.db.commit()

    def write_comments(self, item):
        sql = 'insert into Case_Comments values(%s,%s,%s,%s)'
        Case_Comments=item['Case_Comments']
        if not Case_Comments:
            return
        L=[]
        for i in Case_Comments:
            L.append((item['Case_Number'],i['name'],i['time'],i['content']))
        self.cursor.executemany(sql, L)
        self.db.commit()

    def write_kba_doc(self, item):
        sql = 'insert into Case_KBA_Doc values(%s,%s,%s,%s)'
        Case_KBA_Doc=item['Case_KBA_Doc']
        if not Case_KBA_Doc:
            return
        L=[]
        for i in Case_KBA_Doc:
            L.append((item['Case_Number'],i['link'],i['link'],i['Title']))
        self.cursor.executemany(sql, L)
        self.db.commit()

    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()


class RedisPipeline(object):
    def open_spider(self, spider):
        self.r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

    def process_item(self, item, spider):
        url = item["Case_link"]
        url_md5 = md5(url.encode()).hexdigest()
        self.r.sadd("url", url_md5)
        print("%s 写入redis成功" % url)
        return item

    def close_spider(self, spider):
        pass
