from dataclasses import dataclass
from typing import Optional

import pytest

from src.models.GolfPlayer import GolfPlayer, golf_player_from_dict


class TestGolfPlayer:
    @dataclass
    class Params:
        input: dict
        expected: GolfPlayer
        expected_is_decent_day: bool
        expected_tweet: str
        college_map: Optional[dict]

    @dataclass
    class Fixture:
        actual: GolfPlayer
        expected: GolfPlayer
        expected_is_decent_day: bool
        expected_tweet: str
        actual_tweet: str

    @pytest.fixture(
        ids=['Tied', 'Not Tied', 'Cut'],
        params=[
            Params(
                input={'first_name': 'Bo', 'last_name': 'Jackson', 'id': '1', 'score': 0, 'tied': True, 'position': 2},
                expected=GolfPlayer(
                    id='1',
                    full_name='Bo Jackson',
                    league_name='pga',
                    college='someCollege',
                    score=0,
                    tied=True,
                    position=2,
                    status='PROBABLY_NOT_CUT',
                    rounds=[]
                ),
                expected_is_decent_day=True,
                expected_tweet='Bo Jackson E (T2)',
                college_map={'college': 'someCollege'},
            ),
            Params(
                input={'first_name': 'Bo', 'last_name': 'Jackson', 'id': '1', 'score': 0, 'tied': False, 'position': 2},
                expected=GolfPlayer(
                    id='1',
                    full_name='Bo Jackson',
                    league_name='pga',
                    college='someCollege',
                    score=0,
                    tied=False,
                    position=2,
                    status='PROBABLY_NOT_CUT',
                    rounds=[]
                ),
                expected_is_decent_day=True,
                expected_tweet='Bo Jackson E (2)',
                college_map={'college': 'someCollege'},
            ),
            Params(
                input={'first_name': 'Bo', 'last_name': 'Jackson', 'id': '1', 'score': 0, 'tied': False, 'position': 2, 'status': 'CUT'},
                expected=GolfPlayer(
                    id='1',
                    full_name='Bo Jackson',
                    league_name='pga',
                    college='someCollege',
                    score=0,
                    tied=False,
                    position=2,
                    status='CUT',
                    rounds=[]
                ),
                expected_is_decent_day=False,
                expected_tweet='Bo Jackson E (2)',
                college_map={'college': 'someCollege'},
            )
        ]
    )
    def setup(self, request):
        actual = golf_player_from_dict(
            player=request.param.input,
            league_name=request.param.expected.league_name,
            college=request.param.college_map
        )
        return TestGolfPlayer.Fixture(
            actual=actual,
            expected=request.param.expected,
            expected_is_decent_day=request.param.expected_is_decent_day,
            expected_tweet=request.param.expected_tweet,
            actual_tweet=actual.convert_to_tweet()
        )

    def test_object_correct(self, setup: Fixture):
        assert setup.actual == setup.expected

    def test_is_decent_day(self, setup: Fixture):
        assert setup.actual.has_stats() == setup.expected_is_decent_day

    def test_convert_to_tweet(self, setup: Fixture):
        assert setup.actual_tweet == setup.expected_tweet
