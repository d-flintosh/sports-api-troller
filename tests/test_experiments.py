import pytest
import statsapi
from nba_api.stats.library.parameters import LeagueID
from datetime import date
from src.basketball import get_basketball
from src.mlb import get_mlb


@pytest.mark.skip(reason="only run this manually")
def test_mlb():
    get_mlb(date(2021, 6, 11), send_message=False)


@pytest.mark.skip(reason="only run this manually")
def test_get_basketball():
    get_basketball(date(2021, 6, 12), send_message=False, league_id=LeagueID.nba)


@pytest.mark.skip(reason="only run this manually")
def test_get_mlb_teams_from_api():
    print(statsapi.lookup_team(''))