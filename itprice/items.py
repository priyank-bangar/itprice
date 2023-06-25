# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ItpriceItem(scrapy.Item):
    # define the fields for your item here like:
    product_number = scrapy.Field()
    description = scrapy.Field()
    list_price = scrapy.Field()
    our_price = scrapy.Field()
