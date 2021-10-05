from typing import List

import pandas

from src.extraction.League import League
from src.models.SendTweetForSchool import SendTweetForSchool
from src.models.TweetObject import TweetObject
from src.universal import update_tweet_checkpoint, get_previously_published_games


def tweet_driver(leagues: List[League], date_to_run, send_message: bool, skip_filter: bool):
    for league in leagues:
        try:
            games_published = []
            games = league.get_games(date=date_to_run)
            previously_published_games = get_previously_published_games(date=date_to_run, league_name=league.league_name)
            filtered_games = list(filter(
                lambda x: skip_filter or league.get_game_id(game=x) not in previously_published_games, games)
            )
            games_published = games_published + previously_published_games
            tweetable_objects: [TweetObject] = []

            for game in filtered_games:
                game_id = league.get_game_id(game=game)

                this_games_tweets = league.get_tweetable_objects(game=game)
                games_published.append(game_id)
                tweetable_objects = tweetable_objects + this_games_tweets

            if tweetable_objects:
                df = pandas.DataFrame([vars(s) for s in tweetable_objects]).groupby('tweet_path')

                for school_group in df:
                    school = school_group[0]
                    player_stats = school_group[1]["player_object"].to_list()

                    SendTweetForSchool(
                        school=str(school),
                        player_stats=player_stats,
                        send_message=send_message
                    ).publish(
                        sport=league.sport,
                        league_name=league.league_name
                    )

                update_tweet_checkpoint(
                    league_name=league.league_name,
                    send_message=send_message,
                    date=date_to_run,
                    games_published=games_published
                )
        except Exception as e:
            print(str(e))
