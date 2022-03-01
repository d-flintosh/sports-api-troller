from datetime import timedelta, datetime

import pytz

from src.api.lpga_sport_radar import LpgaSportRadar
from src.api.mlb_sport_radar import MlbSportRadar
from src.api.nba_sport_radar import NbaSportRadar
from src.api.nfl_sport_radar import NflSportRadar
from src.api.nhl_sport_radar import NhlSportRadar
from src.api.pga_sport_radar import PgaSportRadar
from src.api.sport_radar import SportRadarApi
from src.api.wnba_sport_radar import WnbaSportRadar
from src.extraction.BaseballLeague import BaseballLeague
from src.extraction.BasketballLeague import BasketballLeague
from src.extraction.FootballLeague import FootballLeague
from src.extraction.GolfLeague import GolfLeague
from src.extraction.HockeyLeague import HockeyLeague
from src.tweet_driver import tweet_driver


def entrypoint(event, context):
    time_delta = int(event.get('attributes', {}).get('time_delta', '24'))
    task_type = event.get('attributes', {}).get('task_type', 'recent_events')

    if task_type == 'recent_events':
        api_client = SportRadarApi()
        tz = pytz.timezone('America/Chicago')
        chicago_now = datetime.now(tz)
        date_to_run = chicago_now - timedelta(hours=time_delta)
        leagues = []
        if time_delta == 24:
            skip_filter = True
            leagues.append(GolfLeague(league_name='pga', league_client=PgaSportRadar(api_client=api_client)))
            leagues.append(GolfLeague(league_name='lpga', league_client=LpgaSportRadar(api_client=api_client)))
        else:
            skip_filter = False
            leagues.append(BaseballLeague(league_client=MlbSportRadar(api_client=api_client)))
            leagues.append(BasketballLeague(league_name='nba', league_client=NbaSportRadar(api_client=api_client)))
            leagues.append(BasketballLeague(league_name='wnba', league_client=WnbaSportRadar(api_client=api_client)))
            leagues.append(HockeyLeague(league_name='nhl', league_client=NhlSportRadar(api_client=api_client)))
            leagues.append(FootballLeague(league_name='nfl', league_client=NflSportRadar(api_client=api_client)))

        tweet_driver(leagues=leagues, date_to_run=date_to_run.date(), send_message=True, skip_filter=skip_filter)
    elif task_type == 'published_message':
        print('I got a message')
