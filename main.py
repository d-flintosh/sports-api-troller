from datetime import date, timedelta

from nba_api.stats.library.parameters import LeagueID

from src.basketball import get_basketball
from src.mlb import get_mlb


def entrypoint(event, context):
    yesterday = date.today() - timedelta(1)

    # get_mlb(date_to_run=yesterday, send_message=True)
    get_basketball(date_to_run=yesterday, league_id=LeagueID.nba, send_message=False)
    # get_basketball(date_to_run=yesterday, league_id=LeagueID.wnba, send_message=True)

