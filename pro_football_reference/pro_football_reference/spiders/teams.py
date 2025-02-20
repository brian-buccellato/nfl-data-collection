import re
import scrapy
from collections.abc import Iterable, Generator
from typing import Any
from datetime import datetime

import scrapy.http
from pro_football_reference.utils.pfr_base import ProFootballReferenceBase
from pro_football_reference.utils.pfr_table_config import (
    TEAM_STATS_AND_RANKINGS_CONFIG,
    TEAM_CONVERSIONS_CONFIG,
    PLAYER_CONFIG,
)
from pro_football_reference.settings import TEAM_ABBREVIATIONS
from pro_football_reference.items import (
    TeamStatsAndRankingsItem,
    TeamConversionsItem,
    PlayerPasserItem,
    PlayerRusherAndReceivingItem,
    PlayerPuntAndKickReturnerItem,
    PlayerDefenseAndFumblesItem,
    PlayerKickerItem,
    PlayerPunterItem,
)


class TeamsPageSpider(ProFootballReferenceBase):
    name = "teams_page"
    config = [
        {
            "item_class": TeamStatsAndRankingsItem,
            "table_selector": "#team_stats > tbody > tr",
            "stats_config": TEAM_STATS_AND_RANKINGS_CONFIG,
        },
        {
            "item_class": TeamConversionsItem,
            "table_selector": "#team_conversions > tbody > tr",
            "stats_config": TEAM_CONVERSIONS_CONFIG,
        },
        {
            "item_class": PlayerPasserItem,
            "table_selector": "#passing > tbody > tr",
            "stats_config": PLAYER_CONFIG,
            "link_selector": "td[data-stat='name_display'] a::attr(href)",
        },
        {
            "item_class": PlayerRusherAndReceivingItem,
            "table_selector": "#rushing_and_receiving > tbody > tr",
            "stats_config": PLAYER_CONFIG,
            "link_selector": "td[data-stat='name_display'] a::attr(href)",
        },
        {
            "item_class": PlayerPuntAndKickReturnerItem,
            "table_selector": "#returns > tbody > tr",
            "stats_config": PLAYER_CONFIG,
            "link_selector": "td[data-stat='name_display'] a::attr(href)",
        },
        {
            "item_class": PlayerDefenseAndFumblesItem,
            "table_selector": "#defense > tbody > tr",
            "stats_config": PLAYER_CONFIG,
            "link_selector": "td[data-stat='name_display'] a::attr(href)",
        },
        {
            "item_class": PlayerKickerItem,
            "table_selector": "#kicking > tbody > tr",
            "stats_config": PLAYER_CONFIG,
            "link_selector": "td[data-stat='name_display'] a::attr(href)",
        },
        {
            "item_class": PlayerPunterItem,
            "table_selector": "#punting > tbody > tr",
            "stats_config": PLAYER_CONFIG,
            "link_selector": "td[data-stat='name_display'] a::attr(href)",
        },
    ]

    def start_requests(self) -> Iterable[scrapy.Request]:

        self.update_season_year()
        start_urls = [
            f"https://www.pro-football-reference.com/teams/{team}/{self.season_year}.htm"
            for team in TEAM_ABBREVIATIONS
        ]
        for url in start_urls:
            yield scrapy.Request(url, meta={"team": url.split("/")[-2]})

    @classmethod
    def update_settings(cls, settings):
        """This method will set the ITEM_PIPELINES setting for the current spider."""
        settings.set(
            "ITEM_PIPELINES",
            {"pro_football_reference.pipelines.TeamsPagePipeline": 300},
        )
        return settings

    def parse(self, response) -> Generator[TeamStatsAndRankingsItem, Any, None]:
        team = response.meta["team"]
        year = self.season_year

        # Extract table tags
        table_tags = re.findall(
            r"(<table.*?>.*?</table>)", response.text, flags=re.DOTALL
        )

        # Join the extracted table tags into a single string
        cleaned_response_text = "".join(table_tags)

        # Create a new response object with the cleaned response text
        cleaned_response = scrapy.http.HtmlResponse(
            url=response.url, body=cleaned_response_text, encoding="utf-8"
        )
        for c in self.config:
            table = cleaned_response.css(c["table_selector"])
            item = c["item_class"](team=team, year=year)
            if "link_selector" in c:
                for row in table:
                    player_page_link = row.css(c["link_selector"]).get()
                    item["player_link"] = player_page_link
                    item["player_name"] = row.css(
                        "td[data-stat='name_display'] > a::text"
                    ).get()
                    for config in c["stats_config"]:
                        item[config.attr] = self.get_table_item(
                            table=row,
                            data_stat=config.stat,
                            index=config.index,
                            table_part=config.table_part,
                        )
                    yield item
            else:
                for config in c["stats_config"]:
                    item[config.attr] = self.get_table_item(
                        table=table,
                        data_stat=config.stat,
                        index=config.index,
                        table_part=config.table_part,
                    )
                yield item
