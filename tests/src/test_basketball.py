from dataclasses import dataclass
from datetime import date
from typing import List, Optional
from unittest.mock import Mock, call, patch

import pytest

from src.api.basketball_sport_radar import BasketballSportRadar
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
        mock_league_client: Mock
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
                mock_schedule_return=[{'id': '1'}],
                mock_player_stats_return=BasketballPlayer(
                    id='5',
                    league_name='nba',
                    team_id='1',
                    full_name='Dragon',
                    college='FSU',
                    points=1,
                    rebounds=5,
                    assists=0
                ),
                expected_boxscore_calls=[call(game_id='1')],
                expected_basketball_player_from_dict=[
                    call(
                        player={'id': '123'},
                        team_id='5',
                        league_name='nba',
                        college={"id": '123', "college": "someSchool"}
                    ),
                    call(
                        player={'id': '321'},
                        team_id='8',
                        league_name='nba',
                        college=None
                    )
                ]
            )
        ]
    )
    @patch('src.basketball.SendTweetForSchool', autospec=True)
    @patch('src.basketball.basketball_player_from_dict', autospec=True)
    @patch('src.basketball.Gcs', autospec=True)
    def setup(self, mock_gcs, mock_basketball_player, mock_send_tweet, request):
        mock_league_client = Mock(spec=BasketballSportRadar)
        mock_league_client.get_daily_schedule.return_value = {
            'games': request.param.mock_schedule_return
        }
        mock_league_client.get_boxscore.return_value = {
            'home': {
                'id': '5',
                'players': [{
                    'id': '123'
                }]
            },
            'away': {
                'id': '8',
                'players': [{
                    'id': '321'
                }]
            }
        }
        mock_gcs.return_value.read_as_dict.return_value = {'123': {'id': '123', 'college': 'someSchool'}}

        mock_basketball_player.return_value = request.param.mock_player_stats_return

        get_basketball(
            date_to_run=date(2020, 1, 1),
            league_client=mock_league_client,
            league_name='nba',
            send_message=True
        )
        return TestBasketball.Fixture(
            mock_league_client=mock_league_client,
            mock_gcs=mock_gcs,
            expected_boxscore_calls=request.param.expected_boxscore_calls,
            mock_basketball_player=mock_basketball_player,
            expected_basketball_player_from_dict=request.param.expected_basketball_player_from_dict,
            mock_send_tweet=mock_send_tweet
        )

    def test_basketball_player_from_dict_called(self, setup: Fixture):
        setup.mock_basketball_player.assert_has_calls(setup.expected_basketball_player_from_dict)

    def test_schedule_called(self, setup: Fixture):
        setup.mock_league_client.get_daily_schedule.assert_called_once_with(date=date(2020, 1, 1))

    def test_boxscore_called(self, setup: Fixture):
        setup.mock_league_client.get_boxscore.assert_has_calls(setup.expected_boxscore_calls)

    def test_gcs_constructor_called(self, setup: Fixture):
        setup.mock_gcs.assert_called_once_with('college-by-player')

    def test_read_as_dict_called(self, setup: Fixture):
        setup.mock_gcs.return_value.read_as_dict.assert_called_once_with(url='nba/players.json')

    def test_send_tweet_constructor_called(self, setup: Fixture):
        if setup.expected_basketball_player_from_dict:
            mock_palyer = BasketballPlayer(id='5', league_name='nba', team_id='1', full_name='Dragon', college='FSU',
                                           points=1, rebounds=5, assists=0)
            setup.mock_send_tweet.assert_called_once_with(
                school='fsu', player_stats=[mock_palyer, mock_palyer])
        else:
            setup.mock_send_tweet.assert_not_called()

    def test_send_tweet_publish_called(self, setup: Fixture):
        if setup.expected_basketball_player_from_dict:
            setup.mock_send_tweet.return_value.publish.assert_called_once_with(send_message=True, sport='basketball')
        else:
            setup.mock_send_tweet.return_value.publish.assert_not_called()
