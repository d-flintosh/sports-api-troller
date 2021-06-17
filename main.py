from datetime import date, timedelta

from src.api.nba_sport_radar import NbaSportRadar
from src.api.sport_radar import SportRadarApi
from src.api.wnba_sport_radar import WnbaSportRadar
from src.basketball import get_basketball
from src.mlb import get_mlb


def entrypoint(event, context):
    yesterday = date.today() - timedelta(1)

    get_mlb(date_to_run=yesterday, send_message=True)
    api_client = SportRadarApi()
    nba_client = NbaSportRadar(api_client=api_client)
    wnba_client = WnbaSportRadar(api_client=api_client)

    get_basketball(date_to_run=yesterday, league_name='nba', league_client=nba_client, send_message=True)
    get_basketball(date_to_run=yesterday, league_name='wnba', league_client=wnba_client, send_message=True)

