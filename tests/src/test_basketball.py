from dataclasses import dataclass
from typing import List, Optional
from unittest.mock import Mock, call, patch
from datetime import date

import pytest
from nba_api.stats.library.parameters import LeagueID

from src.basketball import get_basketball
from src.models.BasketballPlayer import BasketballPlayer


class TestBasketball:
    @dataclass
    class Params:
        mock_schedule_return: List
        mock_player_stats_return: Optional[BasketballPlayer]
        expected_boxscore_calls: List
        expected_basketball_player_from_dict: List

    @dataclass
    class Fixture:
        mock_boxscore: Mock
        mock_scoreboard: Mock
        mock_gcs: Mock
        expected_boxscore_calls: List
        mock_basketball_player: Mock
        expected_basketball_player_from_dict: List
        mock_send_tweet: Mock

    @pytest.fixture(
        ids=['No games found', 'Game and Players Found'],
        params=[
            Params(
                mock_schedule_return=[],
                mock_player_stats_return=None,
                expected_boxscore_calls=[],
                expected_basketball_player_from_dict=[]
            ),
            Params(
                mock_schedule_return=[{'GAME_ID': 1}],
                mock_player_stats_return=BasketballPlayer(
                    id=5,
                    full_name='Dragon',
                    college='FSU',
                    points=1,
                    rebounds=5,
                    assists=0
                ),
                expected_boxscore_calls=[call(game_id=1)],
                expected_basketball_player_from_dict=[call(player={'PLAYER_ID': 123}, college={"id": 123, "college": "someSchool"})]
            )
        ]
    )
    @patch('src.basketball.SendTweetForSchool', autospec=True)
    @patch('src.basketball.basketball_player_from_dict', autospec=True)
    @patch('src.basketball.Gcs', autospec=True)
    @patch('src.basketball.scoreboard', autospec=True)
    @patch('src.basketball.boxscoretraditionalv2', autospec=True)
    def setup(self, mock_boxscore, mock_scoreboard, mock_gcs, mock_basketball_player, mock_send_tweet, request):

        mock_schedule = Mock()
        mock_gcs.return_value.read_as_dict.return_value = {"123": {"id": 123, "college": "someSchool"}}
        mock_schedule.get_normalized_dict.return_value = {
            'GameHeader': request.param.mock_schedule_return
        }

        mock_scoreboard.Scoreboard.return_value = mock_schedule

        mock_player_stats = Mock()
        mock_player_stats.get_normalized_dict.return_value = {
            'PlayerStats': [{
                'PLAYER_ID': 123
            }]
        }
        mock_boxscore.BoxScoreTraditionalV2.return_value = mock_player_stats

        mock_basketball_player.return_value = request.param.mock_player_stats_return

        get_basketball(date_to_run=date(2020, 1, 1), league_id=LeagueID.nba, send_message=True)
        return TestBasketball.Fixture(
            mock_boxscore=mock_boxscore,
            mock_scoreboard=mock_scoreboard,
            mock_gcs=mock_gcs,
            expected_boxscore_calls=request.param.expected_boxscore_calls,
            mock_basketball_player=mock_basketball_player,
            expected_basketball_player_from_dict=request.param.expected_basketball_player_from_dict,
            mock_send_tweet=mock_send_tweet
        )

    def test_basketball_player_from_dict_called(self, setup: Fixture):
        setup.mock_basketball_player.assert_has_calls(setup.expected_basketball_player_from_dict)

    def test_scoreboard_called(self, setup: Fixture):
        setup.mock_scoreboard.Scoreboard.assert_called_once_with(game_date='01/01/2020', league_id=LeagueID.nba)

    def test_boxscore_called(self, setup: Fixture):
        setup.mock_boxscore.BoxScoreTraditionalV2.assert_has_calls(setup.expected_boxscore_calls)

    def test_read_as_dict_called(self, setup: Fixture):
        setup.mock_gcs.return_value.read_as_dict.assert_called_once_with(url='nba/players.json')

    def test_send_tweet_constructor_called(self, setup: Fixture):
        if setup.expected_basketball_player_from_dict:
            setup.mock_send_tweet.assert_called_once_with(school='fsu', player_stats=[BasketballPlayer(
                id=5,
                full_name='Dragon',
                college='FSU',
                points=1,
                rebounds=5,
                assists=0
            )])
        else:
            setup.mock_send_tweet.assert_not_called()

    def test_send_tweet_publish_called(self, setup: Fixture):
        if setup.expected_basketball_player_from_dict:
            setup.mock_send_tweet.return_value.publish.assert_called_once_with(send_message=True, sport='basketball')
        else:
            setup.mock_send_tweet.return_value.publish.assert_not_called()
