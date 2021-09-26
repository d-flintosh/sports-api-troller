from dataclasses import dataclass
from unittest.mock import Mock, patch

import pytest

from src.models.FootballPlayer import FootballPlayer, football_player_from_dict
from src.models.MlbTeams import mlb_team_map
from src.models.NflTeams import nfl_team_map


class TestFootballPlayer:
    @dataclass
    class Params:
        input: dict
        expected: FootballPlayer
        expected_has_stats: bool
        expected_had_a_great_day: bool
        expected_tweet: str

    @dataclass
    class Fixture:
        actual: FootballPlayer
        expected: FootballPlayer
        expected_has_stats: bool
        expected_had_a_great_day: bool
        expected_tweet: str
        mock_get_team_text: Mock
        actual_tweet: str

    @pytest.fixture(
        ids=['All Stats'],
        params=[
            Params(
                input={
                    'team_id': '1',
                    'player_id': '1',
                    'full_name': 'Bo Jack',
                    'rushing': {
                        'attempts': 1,
                        'yards': 10,
                        'touchdowns': 2
                    },
                    'receiving': {
                        'receptions': 3,
                        'yards': 11,
                        'touchdowns': 4
                    },
                    'passing': {
                        'attempts': 5,
                        'completions': 6,
                        'yards': 12,
                        'touchdowns': 7
                    },
                    'defense': {
                        'sacks': 4.5,
                        'tackles': 9,
                        'interceptions': 3,
                        'forced_fumbles': 9,
                        'fumble_recoveries': 4,
                        'passes_defended': 9
                    },
                    'field_goals': {
                        'made': 3,
                        'attempts': 4
                    }
                },
                expected=FootballPlayer(
                    id='1',
                    full_name='Bo Jack',
                    team_id='1',
                    college='someCollege',
                    rushing_attempts=1,
                    rushing_yards=10,
                    rushing_td=2,
                    receiving_receptions=3,
                    receiving_yards=11,
                    receiving_td=4,
                    passing_attempts=5,
                    passing_completions=6,
                    passing_td=7,
                    passing_yards=12,
                    def_sacks=4.5,
                    def_tackles=9,
                    def_int=3,
                    def_ff=9,
                    def_fr=4,
                    def_pd=9,
                    fg_made=3,
                    fg_attempts=4,
                    league_name='nfl'
                ),
                expected_has_stats=True,
                expected_had_a_great_day=True,
                expected_tweet='Bo Jack (#some team) 1 ATT/10 YDS/2 TD. 3 REC/11 YDS/4 TD. 6-5 12 YDS/7 TD. 9 TAK/4.5 SCK/3 INT/9 FF/4 FR/9 PD. 3/4 FGs'
            )
        ]
    )
    @patch('src.models.FootballPlayer.get_team_text', autospec=True)
    def setup(self, mock_get_team_text, request):
        mock_get_team_text.return_value = ' (#some team)'
        actual = football_player_from_dict(
            player=request.param.input,
            college={'college': 'someCollege'}
        )

        return TestFootballPlayer.Fixture(
            actual=actual,
            expected=request.param.expected,
            expected_has_stats=request.param.expected_has_stats,
            expected_tweet=request.param.expected_tweet,
            mock_get_team_text=mock_get_team_text,
            actual_tweet=actual.convert_to_tweet(),
            expected_had_a_great_day=request.param.expected_had_a_great_day
        )

    def test_object_correct(self, setup: Fixture):
        assert setup.actual == setup.expected

    def test_has_stats(self, setup: Fixture):
        assert setup.actual.has_stats() == setup.expected_has_stats

    def test_had_a_great_day(self, setup: Fixture):
        assert setup.actual.had_a_great_day() == setup.expected_had_a_great_day

    def test_get_team_text_called(self, setup: Fixture):
        setup.mock_get_team_text.assert_called_once_with(team_map=nfl_team_map, team_id='1')

    def test_convert_to_tweet(self, setup: Fixture):
        assert setup.actual_tweet == setup.expected_tweet
