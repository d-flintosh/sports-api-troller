from dataclasses import dataclass
from unittest.mock import Mock, call
from datetime import date
import pytest

from src.api.basketball_sport_radar import BasketballSportRadar
from src.api.mlb_sport_radar import MLB_BASE_URL, MlbSportRadar
from src.api.nba_sport_radar import NBA_BASE_URL
from src.api.sport_radar import SportRadarApi
from src.api.wnba_sport_radar import WNBA_BASE_URL
from src.models.PlayerDraft import PlayerDraft

MOCK_MLB_TEAMS_IN_LEAGUE_RETURN = {
    'leagues': [
        {
            'divisions': [
                {
                    'teams': [
                        {
                            'id': 'id-1'
                        }
                    ]
                },
                {
                    'teams': [
                        {
                            'id': 'id-4'
                        }
                    ]
                }
            ]
        },
        {
            'divisions': [
                {
                    'teams': [
                        {
                            'id': 'id-2'
                        },
                        {
                            'id': 'id-3'
                        }
                    ]
                }
            ]
        }
    ]
}

MOCK_ROSTER_RETURN = {
    'players': [
        {
            'id': '1',
            'full_name': 'Bo',
            'college': 'someCollege'
        }
    ]
}

MOCK_SCHEDULE_RETURN = {
    'games': [{
        'id': 'e70135f7-b822-4a3e-9068-e025c490fd2f',
    }]
}

MOCK_BOXSCORE_RETURN = {
    'foo': 'bar'
}


def mock_make_request(url: str):
    if 'league/hierarchy.json' in url:
        return MOCK_MLB_TEAMS_IN_LEAGUE_RETURN

    if 'teams/' in url:
        return MOCK_ROSTER_RETURN

    if 'schedule.json' in url:
        return MOCK_SCHEDULE_RETURN

    if 'summary.json' in url:
        return MOCK_BOXSCORE_RETURN


class TestMlbSportRadar:
    @dataclass
    class Params:
        league_base_url: str

    @dataclass
    class Fixture:
        mock_api_client: Mock
        subject: MlbSportRadar
        league_base_url: str

    @pytest.fixture
    def setup(self):
        mock_api_client = Mock(spec=SportRadarApi)
        mock_api_client.make_request.side_effect = mock_make_request

        return TestMlbSportRadar.Fixture(
            mock_api_client=mock_api_client,
            league_base_url=MLB_BASE_URL,
            subject=MlbSportRadar(api_client=mock_api_client)
        )

    def test_get_all_team_ids_calls_correct_endpoint(self, setup: Fixture):
        setup.subject.get_all_team_ids()
        setup.mock_api_client.make_request.assert_called_once_with(
            url=f'http://api.sportradar.us/{setup.league_base_url}league/hierarchy.json'
        )

    def test_get_all_team_ids(self, setup: Fixture):
        actual = setup.subject.get_all_team_ids()
        assert ['id-1', 'id-4', 'id-2', 'id-3'] == actual

    def test_get_all_players_with_college(self, setup: Fixture):
        setup.subject.get_all_players_with_college()
        setup.mock_api_client.make_request.assert_has_calls([
            call(url=f'http://api.sportradar.us/{setup.league_base_url}teams/id-1/profile.json'),
            call(url=f'http://api.sportradar.us/{setup.league_base_url}teams/id-4/profile.json'),
            call(url=f'http://api.sportradar.us/{setup.league_base_url}teams/id-2/profile.json'),
            call(url=f'http://api.sportradar.us/{setup.league_base_url}teams/id-3/profile.json')
        ], any_order=True)

    def test_get_all_players_with_college_result(self, setup: Fixture):
        actual = setup.subject.get_all_players_with_college()
        mock_player = PlayerDraft(
            id='1',
            full_name='Bo',
            college='someCollege'
        )
        assert actual == [mock_player, mock_player, mock_player, mock_player]

    def test_get_games_for_date(self, setup: Fixture):
        setup.subject.get_daily_schedule(date=date(2021, 6, 1))
        setup.mock_api_client.make_request.assert_has_calls([
            call(url=f'http://api.sportradar.us/{setup.league_base_url}games/2021/06/01/schedule.json')
        ], any_order=True)

    def test_get_games_for_date_result(self, setup: Fixture):
        actual = setup.subject.get_daily_schedule(date=date(2021, 6, 1))
        assert actual == MOCK_SCHEDULE_RETURN

    def test_get_boxscore(self, setup: Fixture):
        setup.subject.get_boxscore(game_id='1234')
        setup.mock_api_client.make_request.assert_has_calls([
            call(url=f'http://api.sportradar.us/{setup.league_base_url}games/1234/summary.json')
        ], any_order=True)

    def test_get_boxscore_result(self, setup: Fixture):
        actual = setup.subject.get_boxscore(game_id='1234')
        assert actual == MOCK_BOXSCORE_RETURN
