from datetime import date, timedelta

from nba_api.stats.library.parameters import LeagueID

from src.basketball import get_basketball
from src.mlb import get_mlb


def entrypoint(event, context):
    yesterday = date.today() - timedelta(1)

    get_mlb(date_to_run=yesterday)
    get_basketball(date_to_run=yesterday, league_id=LeagueID.nba)
    get_basketball(date_to_run=yesterday, league_id=LeagueID.wnba)

