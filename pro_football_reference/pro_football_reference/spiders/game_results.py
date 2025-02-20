"""
This module will scrape the game results for a given season from Pro Football Reference.
The results are stored in a JSON Lines file in an S3 bucket.
"""

import scrapy
from collections.abc import Iterable, Generator
from typing import Any
from pro_football_reference.items import GameResultItem
from pro_football_reference.utils.pfr_base import ProFootballReferenceBase
from pro_football_reference.utils.pfr_table_config import GAME_RESULTS_CONFIG
from pro_football_reference.settings import S3_BUCKET_NAME


class GameResultsSpider(ProFootballReferenceBase):
    name = "game_results"

    def parse(self, response) -> Generator[GameResultItem, Any, None]:
        for row in response.css("#games > tbody > tr"):
            if game_date := row.css("td[data-stat='game_date']::text").get():
                game_result_item = GameResultItem(
                    year=self.season_year,
                    game_date=game_date,
                    boxscore_link=row.css(
                        "td[data-stat='boxscore_word'] a::attr(href)"
                    ).get(),
                    winner_points=row.css(
                        "td[data-stat='pts_win'] > strong::text"
                    ).get()
                    or row.css("td[data-stat='pts_win']::text").get(),
                )
                for config in GAME_RESULTS_CONFIG:
                    game_result_item[config.attr] = self.get_table_item(
                        table=row,
                        data_stat=config.stat,
                        table_part=config.table_part,
                        index=config.index,
                    )
                yield game_result_item

    def start_requests(self) -> Iterable[scrapy.Request]:
        self.update_season_year()
        self.start_urls = [
            f"https://www.pro-football-reference.com/years/{self.season_year}/games.htm"
        ]
        for url in self.start_urls:
            yield scrapy.Request(url)

    @classmethod
    def update_settings(cls, settings):
        """This method will set the ITEM_PIPELINES setting for the current spider."""
        settings.set(
            "ITEM_PIPELINES",
            {"pro_football_reference.pipelines.GameResultsPipeline": 300},
        )
        return settings
