# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class DoubanItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ranking = Field()
    title = Field()
    director = Field()
    desc = Field()
    rating_num = Field()
    people_count = Field()
    date = Field()
    country = Field()
    category = Field()

