# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CasesystemItem(scrapy.Item):
    # define the fields for your item here like:
    Case_link = scrapy.Field()
    Case_Number = scrapy.Field()
    Account_Name = scrapy.Field()
    Open_Time = scrapy.Field()
    Case_Owner = scrapy.Field()
    Contact_Name = scrapy.Field()
    Country = scrapy.Field()
    Subject = scrapy.Field()
    Description = scrapy.Field()
    PA1 = scrapy.Field()
    PA2 = scrapy.Field()
    PA3 = scrapy.Field()
    OS_Android = scrapy.Field()
    Software_Product = scrapy.Field()
    Resolution_Summary = scrapy.Field()
    ResponsivenessToTheCase = scrapy.Field()
    QualityOfTechnicalSupport = scrapy.Field()
    ProfessionalismOfQCEngineer = scrapy.Field()
    Case_KBA_Doc = scrapy.Field()
    Case_Attachments = scrapy.Field()
    Case_Comments = scrapy.Field()
