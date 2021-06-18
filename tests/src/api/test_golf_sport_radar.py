from dataclasses import dataclass
from unittest.mock import Mock, call
from datetime import date
import pytest

from src.api.basketball_sport_radar import BasketballSportRadar
from src.api.golf_sport_radar import GolfSportRadar
from src.api.nba_sport_radar import NBA_BASE_URL
from src.api.pga_sport_radar import PGA_BASE_URL
from src.api.sport_radar import SportRadarApi
from src.api.wnba_sport_radar import WNBA_BASE_URL
from src.models.PlayerDraft import PlayerDraft


MOCK_SCHEDULE_RETURN = {
    'tournaments': [
        {
            'id': '3e27a2c2-49ac-4f97-a412-a9b73048544f',
            'name': 'RBC Canadian Open',
            'start_date': '2021-06-10',
            'end_date': '2021-06-13',
            'status': 'cancelled',
        },
        {
            'id': '0a4373fe-a2b9-4a9d-ad84-d342dea6b61a',
            'name': 'U.S. Open ',
            'start_date': '2021-06-17',
            'end_date': '2021-06-20',
            'status': 'inprogress'
        },
        {
            'id': 'ae2f825c-f895-451d-ae7c-7872e8af3b5a',
            'name': 'Travelers Championship',
            'start_date': '2021-06-24',
            'end_date': '2021-06-27',
            'status': 'scheduled'
        }
    ]
}

MOCK_LEADERBOARD_RETURN = {
    'foo': 'bar'
}


def mock_make_request(url: str):
    if 'tournaments/schedule.json' in url and PGA_BASE_URL in url:
        return MOCK_SCHEDULE_RETURN

    if 'tournaments/1234/leaderboard.json' in url and PGA_BASE_URL in url:
        return MOCK_LEADERBOARD_RETURN


class TestGolfSportRadar:
    @dataclass
    class Params:
        league_base_url: str

    @dataclass
    class Fixture:
        mock_api_client: Mock
        subject: GolfSportRadar
        league_base_url: str

    @pytest.fixture(
        ids=['PGA'],
        params=[
            Params(
                league_base_url=PGA_BASE_URL
            )
        ])
    def setup(self, request):
        mock_api_client = Mock(spec=SportRadarApi)
        mock_api_client.make_request.side_effect = mock_make_request

        return TestGolfSportRadar.Fixture(
            mock_api_client=mock_api_client,
            league_base_url=request.param.league_base_url,
            subject=GolfSportRadar(api_client=mock_api_client, league_base_url=request.param.league_base_url)
        )

    def test_get_tournament_schedule(self, setup: Fixture):
        assert setup.subject.get_tournament_schedule() == MOCK_SCHEDULE_RETURN

    def test_get_tournament_leaderboard(self, setup: Fixture):
        assert setup.subject.get_tournament_leaderboard('1234') == MOCK_LEADERBOARD_RETURN
