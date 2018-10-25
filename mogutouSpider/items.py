# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MogutouspiderItem(scrapy.Item):

    # 图片url
    img_url = scrapy.Field()
    # 目录名
    folder = scrapy.Field()

