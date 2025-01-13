"""
This module will scrape the game results for a given season from Pro Football Reference.
The results are stored in a JSON Lines file in an S3 bucket.
"""
import scrapy
from collections.abc import Iterable, Generator
from typing import Any
from datetime import datetime
from pro_football_reference.items import GameResultItem


class GameResultsSpider(scrapy.Spider):
    name = "game_results"
    season_year = None
    custom_settings = {}

    def parse(self, response) -> Generator[GameResultItem, Any, None]:
        for row in response.css("#games > tbody > tr"):
            if game_date := row.css("td[data-stat='game_date']::text").get():
              game_result_item = GameResultItem(
                  week=row.css("th[data-stat='week_num']::text").get(),
                  day_of_week=row.css("td[data-stat='game_day_of_week']::text").get(),
                  game_date=game_date,
                  game_time=row.css("td[data-stat='gametime']::text").get(),
                  winning_team=row.css("td[data-stat='winner'] a::text").get(),
                  losing_team=row.css("td[data-stat='loser'] a::text").get(),
                  boxscore_link=row.css("td[data-stat='boxscore_word'] a::attr(href)").get(),
                  winner_points=row.css("td[data-stat='pts_win'] > strong::text").get() or row.css("td[data-stat='pts_win']::text").get(),
                  loser_points=row.css("td[data-stat='pts_lose']::text").get(),
                  winner_yards=row.css("td[data-stat='yards_win']::text").get(),
                  loser_yards=row.css("td[data-stat='yards_lose']::text").get(),
                  winner_turnovers=row.css("td[data-stat='to_win']::text").get(),
                  loser_turnovers=row.css("td[data-stat='to_lose']::text").get(),
              )
              yield game_result_item


    def start_requests(self) -> Iterable[scrapy.Request]:
        if not self.season_year:
            season_year = datetime.now().year
            # current year must be previous year if the month is january through august
            if datetime.now().month < 9:
              season_year -= 1
        else:
            season_year = int(self.season_year)
        
        # key for the uri is righ .  not sure about this other stuff
        self.custom_settings["FEEDS"] = {
            f"s3://pro_football_reference_data/game_results/{season_year}/game_results.json": {
                "format": "jsonlines",
                "encoding": "utf8",
            }
        }
        self.start_urls = [
            f"https://www.pro-football-reference.com/years/{season_year}/games.htm"
        ]
        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=True)
    