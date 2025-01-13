# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProFootballReferenceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class GameResultItem(scrapy.Item):
    week = scrapy.Field()
    day_of_week = scrapy.Field()
    game_date = scrapy.Field()
    game_time = scrapy.Field()
    winning_team = scrapy.Field()
    losing_team = scrapy.Field()
    boxscore_link = scrapy.Field()
    winner_points = scrapy.Field()
    loser_points = scrapy.Field()
    winner_yards = scrapy.Field()
    loser_yards = scrapy.Field()
    winner_turnovers = scrapy.Field()
    loser_turnovers = scrapy.Field()