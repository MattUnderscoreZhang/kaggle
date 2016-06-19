# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DogItem(scrapy.Item):
    # define the fields for your item here like:
    Breed = scrapy.Field()
    Intelligence = scrapy.Field()
    Hypoallergenic = scrapy.Field()
    Popularity     = scrapy.Field()
