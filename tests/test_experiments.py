from datetime import date

import pytest

from src.api.lpga_sport_radar import LpgaSportRadar
from src.api.mlb_sport_radar import MlbSportRadar
from src.api.nba_sport_radar import NbaSportRadar
from src.api.nfl_sport_radar import NflSportRadar
from src.api.nhl_sport_radar import NhlSportRadar
from src.api.pga_sport_radar import PgaSportRadar
from src.api.sport_radar import SportRadarApi
from src.api.wnba_sport_radar import WnbaSportRadar
from src.college.write_players_to_gcs import write_to_file_readable_for_computers
from src.extraction.BaseballLeague import BaseballLeague
from src.extraction.BasketballLeague import BasketballLeague
from src.extraction.FootballLeague import FootballLeague
from src.extraction.HockeyLeague import HockeyLeague
from src.tweet_driver import tweet_driver


@pytest.mark.skip(reason="only run this manually")
def test_daily():
    api_client = SportRadarApi()
    leagues = [
        FootballLeague(league_name='nfl', league_client=NflSportRadar(api_client=api_client))
    ]
    tweet_driver(
        leagues=leagues,
        date_to_run=date(2020, 12, 6),
        send_message=False,
        skip_filter=True
    )


@pytest.mark.skip(reason="only run this manually")
def test_hourly():
    api_client = SportRadarApi()
    leagues = [
        BaseballLeague(league_client=MlbSportRadar(api_client=api_client)),
        BasketballLeague(league_name='nba', league_client=NbaSportRadar(api_client=api_client)),
        BasketballLeague(league_name='wnba', league_client=WnbaSportRadar(api_client=api_client)),
        HockeyLeague(league_name='nhl', league_client=NhlSportRadar(api_client=api_client)),
    ]
    tweet_driver(
        leagues=leagues,
        date_to_run=date(2021, 7, 16),
        send_message=False,
        skip_filter=False
    )


@pytest.mark.skip(reason="only run this manually")
def test_extract_baseball_draft_info():
    api_client = SportRadarApi()
    mlb_client = MlbSportRadar(api_client=api_client)
    write_to_file_readable_for_computers(league='mlb', league_client=mlb_client)


@pytest.mark.skip(reason="only run this manually")
def test_extract_basketball_draft_info():
    api_client = SportRadarApi()
    nba_client = NbaSportRadar(api_client=api_client)
    wnba_client = WnbaSportRadar(api_client=api_client)
    write_to_file_readable_for_computers(league='nba', league_client=nba_client)
    write_to_file_readable_for_computers(league='wnba', league_client=wnba_client)


@pytest.mark.skip(reason="only run this manually")
def test_extract_nhl_draft_info():
    api_client = SportRadarApi()
    nhl_client = NhlSportRadar(api_client=api_client)
    write_to_file_readable_for_computers(league='nhl', league_client=nhl_client)


@pytest.mark.skip(reason="only run this manually")
def test_extract_golf_draft_info():
    api_client = SportRadarApi()
    pga_client = PgaSportRadar(api_client=api_client)
    lpga_client = LpgaSportRadar(api_client=api_client)
    write_to_file_readable_for_computers(league='pga', league_client=pga_client)
    write_to_file_readable_for_computers(league='lpga', league_client=lpga_client)


@pytest.mark.skip(reason="only run this manually")
def test_extract_nfl_draft_info():
    api_client = SportRadarApi()
    nfl_client = NflSportRadar(api_client=api_client)
    write_to_file_readable_for_computers(league='nfl', league_client=nfl_client)
