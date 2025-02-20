import scrapy
from datetime import datetime


class ProFootballReferenceBase(scrapy.Spider):

    season_year: int = datetime.now().year
    override_season_year: int = 1

    def update_season_year(self):
        if datetime.now().month < 9 and int(self.override_season_year):
            self.season_year = int(self.season_year) - 1

    @staticmethod
    def get_table_item(table, data_stat, table_part, index) -> str:
        return (
            table[index].css(f"{table_part}[data-stat='{data_stat}']::text").get()
            if index is not None
            else table.css(f"{table_part}[data-stat='{data_stat}']::text").get()
        )
