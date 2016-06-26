# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class dog_item(scrapy.Item):
    # define the fields for your item here like:
    breed          = scrapy.Field()
    size           = scrapy.Field()
    detail         = scrapy.Field()
# end class dog_item
