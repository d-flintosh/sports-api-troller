from datetime import date, timedelta

from src.api.nba_sport_radar import NbaSportRadar
from src.api.sport_radar import SportRadarApi
from src.api.wnba_sport_radar import WnbaSportRadar


from src.extraction.BaseballLeague import BaseballLeague
from src.extraction.BasketballLeague import BasketballLeague
from src.tweet_driver import tweet_driver


def entrypoint(event, context):
    time_delta = int(event.get('attributes', {}).get('time_delta', '1'))
    yesterday = date.today() - timedelta(time_delta)

    api_client = SportRadarApi()
    leagues = [
        BaseballLeague(),
        BasketballLeague(league_name='nba', league_client=NbaSportRadar(api_client=api_client)),
        BasketballLeague(league_name='wnba', league_client=WnbaSportRadar(api_client=api_client))
    ]

    skip_filter = True if time_delta == 1 else False

    tweet_driver(leagues=leagues, date_to_run=yesterday, send_message=True, skip_filter=skip_filter)

