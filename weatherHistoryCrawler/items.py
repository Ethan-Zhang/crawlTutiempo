# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeatherhistorycrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date = scrapy.Field()
    T = scrapy.Field()
    TM = scrapy.Field()
    Tm = scrapy.Field()
    SLP = scrapy.Field()
    H = scrapy.Field()
    PP = scrapy.Field()
    V = scrapy.Field()
    RA = scrapy.Field()
    SN = scrapy.Field()
    TS = scrapy.Field()
