"""
This module will process each scraped item and
upload them to the appropriate path in an S3 bucket.
"""

import boto3
import polars as pl
import s3fs
from pro_football_reference.items import (
    GameResultItem,
    TeamConversionsItem,
    TeamStatsAndRankingsItem,
    PlayerPasserItem,
    PlayerKickerItem,
    PlayerPunterItem,
    PlayerRusherAndReceivingItem,
    PlayerPuntAndKickReturnerItem,
    PlayerDefenseAndFumblesItem,
)


class ProFootballReferencePipeline:
    def __init__(self, s3_bucket_name, aws_access_key_id, aws_secret_access_key):
        self.s3 = boto3.client(
            "s3",
            region_name="us-east-1",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        self.s3_bucket_name = s3_bucket_name
        self.s3_fs = s3fs.S3FileSystem()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            s3_bucket_name=crawler.settings.get("S3_BUCKET_NAME"),
            aws_access_key_id=crawler.settings.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=crawler.settings.get("AWS_SECRET_ACCESS_KEY"),
        )

    def upload_items_to_s3(self, df, path):
        with self.s3_fs.open(path, "w") as f:
            df.write_ndjson(f)

    def process_item(self, item, spider):
        """This method will determine the item type and add it to the appropriate list."""
        for c in self.config:
            if isinstance(item, c["item_class"]):
                c["items"].append(item)
        return item

    def close_spider(self, spider):
        """This method will determine call the upload method for each item type."""
        # upload the items to the S3 bucket
        for c in self.config:
            df = pl.DataFrame(dict(item) for item in c["items"])
            if not df.is_empty():
              year = df["year"].first()
              path = f"s3://{self.s3_bucket_name}/{c['path']}/{year}/{c['file_name']}"
              self.upload_items_to_s3(df=df, path=path)


class TeamsPagePipeline(ProFootballReferencePipeline):
    """
    This class will upload the appropriate items to
    a given S3 bucket key.
    """

    config = [
        {
            "item_class": TeamStatsAndRankingsItem,
            "items": [],
            "path": "team_stats_and_rankings",
            "file_name": "team_stats_and_rankings.json",
        },
        {
            "item_class": TeamConversionsItem,
            "items": [],
            "path": "team_conversions",
            "file_name": "team_conversions.json",
        },
        {
            "item_class": PlayerPasserItem,
            "items": [],
            "path": "player_passer",
            "file_name": "player_passer.json",
        },
        {
            "item_class": PlayerRusherAndReceivingItem,
            "items": [],
            "path": "player_rusher_and_receiver",
            "file_name": "player_rusher_and_receiver.json",
        },
        {
            "item_class": PlayerPuntAndKickReturnerItem,
            "items": [],
            "path": "player_punt_and_kick_returner",
            "file_name": "player_punt_and_kick_returner.json",
        },
        {
            "item_class": PlayerDefenseAndFumblesItem,
            "items": [],
            "path": "player_defense_and_fumbles",
            "file_name": "player_defense_and_fumbles.json",
        },
        {
            "item_class": PlayerKickerItem,
            "items": [],
            "path": "player_kicker",
            "file_name": "player_kicker.json",
        },
        {
            "item_class": PlayerPunterItem,
            "items": [],
            "path": "player_punter",
            "file_name": "player_punter.json",
        },
    ]


class GameResultsPipeline(ProFootballReferencePipeline):
    """This class will upload the game results items to a given S3 bucket key."""

    config = [
        {
            "item_class": GameResultItem,
            "items": [],
            "path": "game_results",
            "file_name": "game_results.json",
        }
    ]
