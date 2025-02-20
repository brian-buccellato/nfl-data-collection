# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GameResultItem(scrapy.Item):
    year = scrapy.Field()
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


class TeamStatsAndRankingsItem(scrapy.Item):
    team = scrapy.Field()
    year = scrapy.Field()
    points_for = scrapy.Field()
    points_against = scrapy.Field()
    yards_for = scrapy.Field()
    yards_against = scrapy.Field()
    passing_first_downs = scrapy.Field()
    passing_first_downs_against = scrapy.Field()
    rushing_first_downs = scrapy.Field()
    rushing_first_downs_against = scrapy.Field()
    completions = scrapy.Field()
    completions_against = scrapy.Field()
    attempts = scrapy.Field()
    attempts_against = scrapy.Field()
    passing_yards = scrapy.Field()
    passing_yards_against = scrapy.Field()
    passing_touchdowns = scrapy.Field()
    passing_touchdowns_against = scrapy.Field()
    interceptions_for = scrapy.Field()
    interceptions_against = scrapy.Field()
    net_yards_per_pass_attempt = scrapy.Field()
    net_yards_per_pass_attempt_against = scrapy.Field()
    rushing_attempts = scrapy.Field()
    rushing_attempts_against = scrapy.Field()
    rushing_yards = scrapy.Field()
    rushing_yards_against = scrapy.Field()
    rushing_touchdowns = scrapy.Field()
    rushing_touchdowns_against = scrapy.Field()
    net_yards_per_rush_attempt = scrapy.Field()
    net_yards_per_rush_attempt_against = scrapy.Field()
    penalties = scrapy.Field()
    opponent_penalties = scrapy.Field()
    penalty_yards = scrapy.Field()
    opponent_penalty_yards = scrapy.Field()
    first_downs_from_penalties = scrapy.Field()
    opponent_first_downs_from_penalties = scrapy.Field()
    number_of_drives = scrapy.Field()
    opponent_number_of_drives = scrapy.Field()
    percentage_of_drives_ending_in_score = scrapy.Field()
    opponent_percentage_of_drives_ending_in_score = scrapy.Field()
    percentage_of_drives_ending_in_turnover = scrapy.Field()
    average_starting_field_position = scrapy.Field()
    opponent_average_starting_field_position = scrapy.Field()
    time_per_drive = scrapy.Field()
    opponent_time_per_drive = scrapy.Field()
    plays_per_drive = scrapy.Field()
    opponent_plays_per_drive = scrapy.Field()
    yards_per_drive = scrapy.Field()
    opponent_yards_per_drive = scrapy.Field()
    points_per_drive = scrapy.Field()
    opponent_points_per_drive = scrapy.Field()

class TeamsPageBaseItem(scrapy.Item):
    team = scrapy.Field()
    year = scrapy.Field()

class TeamConversionsItem(TeamsPageBaseItem):
    third_down_conversions = scrapy.Field()
    third_down_attempts = scrapy.Field()
    third_down_conversions_against = scrapy.Field()
    third_down_attempts_against = scrapy.Field()
    third_down_conversion_percentage = scrapy.Field()
    third_down_conversion_percentage_against = scrapy.Field()
    fourth_down_conversions = scrapy.Field()
    fourth_down_attempts = scrapy.Field()
    fourth_down_conversion_percentage = scrapy.Field()
    fourth_down_conversions_against = scrapy.Field()
    fourth_down_attempts_against = scrapy.Field()
    fourth_down_conversion_percentage_against = scrapy.Field()
    red_zone_conversions = scrapy.Field()
    red_zone_attempts = scrapy.Field()
    red_zone_conversion_percentage = scrapy.Field()
    red_zone_conversions_against = scrapy.Field()
    red_zone_attempts_against = scrapy.Field()
    red_zone_conversion_percentage_against = scrapy.Field()


class PlayerItem(TeamsPageBaseItem):
    position = scrapy.Field()
    player_name = scrapy.Field()
    player_age = scrapy.Field()
    player_link = scrapy.Field()


class PlayerPasserItem(PlayerItem):
    pass


class PlayerRusherAndReceivingItem(PlayerItem):
    pass


class PlayerPuntAndKickReturnerItem(PlayerItem):
    games_started = scrapy.Field()
    punt_returns = scrapy.Field()
    punt_return_yards = scrapy.Field()
    punt_return_touchdowns = scrapy.Field()
    punt_return_long = scrapy.Field()
    punt_return_yards_per_return = scrapy.Field()
    kick_returns = scrapy.Field()
    kick_return_yards = scrapy.Field()
    kick_return_touchdowns = scrapy.Field()
    kick_return_long = scrapy.Field()
    kick_return_yards_per_return = scrapy.Field()
    all_purpose_yards = scrapy.Field()
    awards = scrapy.Field()


class PlayerKickerItem(PlayerItem):
    pass


class PlayerPunterItem(PlayerItem):
    pass


class PlayerDefenseAndFumblesItem(PlayerItem):
    pass
