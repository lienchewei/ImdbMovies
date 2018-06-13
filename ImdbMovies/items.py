# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbmoviesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = scrapy.Field()
    title = scrapy.Field()
    rate = scrapy.Field()
    duration = scrapy.Field()
    director = scrapy.Field()
    stars = scrapy.Field()
    photos = scrapy.Field()
    actors = scrapy.Field()
    storyline = scrapy.Field()
    genres = scrapy.Field()
    country = scrapy.Field()
    language = scrapy.Field()
    releaseDate = scrapy.Field()
    production = scrapy.Field()
    distributor = scrapy.Field()
