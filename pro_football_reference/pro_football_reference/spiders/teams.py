import scrapy
from collections.abc import Iterable, Generator
from typing import Any
from datetime import datetime
from pro_football_reference.settings import TEAM_ABBREVIATIONS
from pro_football_reference.items import TeamStatsAndRankingsItem


class TeamsPageSpider(scrapy.Spider):
    name = "teams_page"
    season_year = datetime.now().year

    def start_requests(self) -> Iterable[scrapy.Request]:
        season_year = int(self.season_year)
        start_urls = [
            f"https://www.pro-football-reference.com/teams/{team}/{season_year}.htm"
            for team in TEAM_ABBREVIATIONS
        ]
        for url in start_urls:
            yield scrapy.Request(url, meta={"team": url.split("/")[-2]})

    @classmethod
    def update_settings(cls, settings):
        """This method will set the ITEM_PIPELINES setting for the current spider."""
        if datetime.now().month < 9:
            cls.season_year -= 1
        settings.set(
            "ITEM_PIPELINES",
            {"pro_football_reference.pipelines.TeamsPagePipeline": 300},
        )
        return settings
    
    def parse(self, response) -> Generator[TeamStatsAndRankingsItem, Any, None]:
        
        team = response.meta["team"]
        year = self.season_year
        
        team_stats_and_rankings_table = response.css("#team_stats > tbody > tr")
        team_stats_and_rankings_item = TeamStatsAndRankingsItem(
            team=team,
            year=year,
            points_for=team_stats_and_rankings_table[0].css("td[data-stat='points']::text").get(),
            points_against=team_stats_and_rankings_table[1].css("td[data-stat='points_opp']::text").get(),
            yards_for=team_stats_and_rankings_table[0].css("td[data-stat='total_yards']::text").get(),
            yards_against=team_stats_and_rankings_table[1].css("td[data-stat='total_yards']::text").get(),
            passing_first_downs=team_stats_and_rankings_table[0].css("td[data-stat='pass_fd']::text").get(),
            passing_first_downs_against=team_stats_and_rankings_table[1].css("td[data-stat='pass_fd']::text").get(),
            completions=team_stats_and_rankings_table[0].css("td[data-stat='pass_cmp']::text").get(),
            completions_against=team_stats_and_rankings_table[1].css("td[data-stat='pass_cmp']::text").get(),
            attempts=team_stats_and_rankings_table[0].css("td[data-stat='pass_att']::text").get(),
            attempts_against=team_stats_and_rankings_table[1].css("td[data-stat='pass_att']::text").get(),
            passing_yards=team_stats_and_rankings_table[0].css("td[data-stat='pass_yds']::text").get(),
            passing_yards_against=team_stats_and_rankings_table[1].css("td[data-stat='pass_yds']::text").get(),
            passing_touchdowns=team_stats_and_rankings_table[0].css("td[data-stat='pass_td']::text").get(),
            passing_touchdowns_against=team_stats_and_rankings_table[1].css("td[data-stat='pass_td']::text").get(),
            interceptions_for=team_stats_and_rankings_table[0].css("td[data-stat='pass_int']::text").get(),
            interceptions_against=team_stats_and_rankings_table[1].css("td[data-stat='pass_int']::text").get(),
            net_yards_per_pass_attempt=team_stats_and_rankings_table[0].css("td[data-stat='pass_net_yds_per_att']::text").get(),
            net_yards_per_pass_attempt_against=team_stats_and_rankings_table[1].css("td[data-stat='pass_net_yds_per_att']::text").get(),
            rushing_attempts=team_stats_and_rankings_table[0].css("td[data-stat='rush_att']::text").get(),
            rushing_attempts_against=team_stats_and_rankings_table[1].css("td[data-stat='rush_att']::text").get(),
            rushing_yards=team_stats_and_rankings_table[0].css("td[data-stat='rush_yds']::text").get(),
            rushing_yards_against=team_stats_and_rankings_table[1].css("td[data-stat='rush_yds']::text").get(),
            rushing_touchdowns=team_stats_and_rankings_table[0].css("td[data-stat='rush_td']::text").get(),
            rushing_touchdowns_against=team_stats_and_rankings_table[1].css("td[data-stat='rush_td']::text").get(),
            net_yards_per_rush_attempt=team_stats_and_rankings_table[0].css("td[data-stat='rush_yds_per_att']::text").get(),
            net_yards_per_rush_attempt_against=team_stats_and_rankings_table[1].css("td[data-stat='rush_yds_per_att']::text").get(),
            penalties=team_stats_and_rankings_table[0].css("td[data-stat='penalties']::text").get(),
            opponent_penalties=team_stats_and_rankings_table[1].css("td[data-stat='penalties']::text").get(),
            penalty_yards=team_stats_and_rankings_table[0].css("td[data-stat='penalties_yds']::text").get(),
            opponent_penalty_yards=team_stats_and_rankings_table[1].css("td[data-stat='penalties_yds']::text").get(),
            first_downs_from_penalties=team_stats_and_rankings_table[0].css("td[data-stat='pen_fd']::text").get(),
            opponent_first_downs_from_penalties=team_stats_and_rankings_table[1].css("td[data-stat='pen_fd']::text").get(),
            number_of_drives=team_stats_and_rankings_table[0].css("td[data-stat='drives']::text").get(),
            opponent_number_of_drives=team_stats_and_rankings_table[1].css("td[data-stat='drives']::text").get(),
            percentage_of_drives_ending_in_score=team_stats_and_rankings_table[0].css("td[data-stat='score_pct']::text").get(),
            opponent_percentage_of_drives_ending_in_score=team_stats_and_rankings_table[1].css("td[data-stat='score_pct']::text").get(),
            percentage_of_drives_ending_in_turnover=team_stats_and_rankings_table[0].css("td[data-stat='turnover_pct']::text").get(),
            average_starting_field_position=team_stats_and_rankings_table[0].css("td[data-stat='start_avg']::text").get(),
            opponent_average_starting_field_position=team_stats_and_rankings_table[1].css("td[data-stat='start_avg']::text").get(),
            time_per_drive=team_stats_and_rankings_table[0].css("td[data-stat='time_avg']::text").get(),
            opponent_time_per_drive=team_stats_and_rankings_table[1].css("td[data-stat='time_avg']::text").get(),
            plays_per_drive=team_stats_and_rankings_table[0].css("td[data-stat='plays_per_drive']::text").get(),
            opponent_plays_per_drive=team_stats_and_rankings_table[1].css("td[data-stat='plays_per_drive']::text").get(),
            yards_per_drive=team_stats_and_rankings_table[0].css("td[data-stat='yds_per_drive']::text").get(),
            opponent_yards_per_drive=team_stats_and_rankings_table[1].css("td[data-stat='yds_per_drive']::text").get(),
            points_per_drive=team_stats_and_rankings_table[0].css("td[data-stat='points_avg']::text").get(),
            opponent_points_per_drive=team_stats_and_rankings_table[1].css("td[data-stat='points_avg']::text").get(),
        )
        yield team_stats_and_rankings_item
        

