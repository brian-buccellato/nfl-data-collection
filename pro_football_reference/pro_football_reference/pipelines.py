# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import boto3
import polars as pl
import s3fs
from pro_football_reference.items import TeamStatsAndRankingsItem
from itemadapter import ItemAdapter


class ProFootballReferencePipeline:
    def process_item(self, item, spider):
        return item


class TeamsPagePipeline:
    """
    This class will upload the appropriate items to
    a given S3 bucket key for the appropriate item
    """

    def __init__(self, s3_bucket_name, aws_access_key_id, aws_secret_access_key):
        self.s3 = boto3.client(
            "s3",
            region_name="us-east-1",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        self.s3_bucket_name = s3_bucket_name
        self.team_stats_and_rankings_items = []
        self.s3_fs = s3fs.S3FileSystem()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            s3_bucket_name=crawler.settings.get("S3_BUCKET_NAME"),
            aws_access_key_id=crawler.settings.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=crawler.settings.get("AWS_SECRET_ACCESS_KEY"),
        )

    def process_item(self, item, spider):
        """This method will determine the item type and add it to the appropriate list."""
        if isinstance(item, TeamStatsAndRankingsItem):
            self.team_stats_and_rankings_items.append(item)
        return item

    def close_spider(self, spider):
        """This method will determine call the upload method for each item type."""
        # upload the items to the S3 bucket
        team_stats_and_rankings_df = pl.DataFrame(dict(item) for item in self.team_stats_and_rankings_items)
        team_stats_and_rankings_year = team_stats_and_rankings_df["year"].first()
        team_stats_and_rankings_path = f"s3://{self.s3_bucket_name}/team_stats_and_rankings/{team_stats_and_rankings_year}/team_stats_and_rankings.json"
        self.upload_items_to_s3(df=team_stats_and_rankings_df, path=team_stats_and_rankings_path)
    
    def upload_items_to_s3(self, df, path):
        with self.s3_fs.open(path, "w") as f:
            df.write_ndjson(f)
