from datetime import date

import pytest
import statsapi

from src.api.nba_sport_radar import NbaSportRadar
from src.api.sport_radar import SportRadarApi
from src.api.wnba_sport_radar import WnbaSportRadar
from src.college.basketball import write_to_file_readable_for_computers
from src.extraction.BasketballLeague import BasketballLeague
from src.extraction.BaseballLeague import BaseballLeague
from src.tweet_driver import tweet_driver


@pytest.mark.skip(reason="only run this manually")
def test_mlb():
    api_client = SportRadarApi()
    leagues = [
        BaseballLeague(),
        BasketballLeague(league_name='nba', league_client=NbaSportRadar(api_client=api_client)),
        BasketballLeague(league_name='wnba', league_client=WnbaSportRadar(api_client=api_client))
    ]
    tweet_driver(leagues=leagues, date_to_run=date(2021, 6, 17), send_message=False)


@pytest.mark.skip(reason="only run this manually")
def test_get_basketball():
    api_client = SportRadarApi()
    nba_client = NbaSportRadar(api_client=api_client)
    wnba_client = WnbaSportRadar(api_client=api_client)

    get_basketball(date(2021, 6, 17), send_message=False, league_name='nba', league_client=nba_client)
    get_basketball(date(2021, 6, 17), send_message=False, league_name='wnba', league_client=wnba_client)


@pytest.mark.skip(reason="only run this manually")
def test_get_mlb_teams_from_api():
    print(statsapi.lookup_team(''))


@pytest.mark.skip(reason="only run this manually")
def test_extract_basketball_draft_info():
    api_client = SportRadarApi()
    nba_client = NbaSportRadar(api_client=api_client)
    wnba_client = WnbaSportRadar(api_client=api_client)
    write_to_file_readable_for_computers(league='nba', league_client=nba_client)
    write_to_file_readable_for_computers(league='wnba', league_client=wnba_client)
