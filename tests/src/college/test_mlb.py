from dataclasses import dataclass
from typing import List, Set
from unittest.mock import patch, Mock, call, mock_open

import pytest

from src.college.mlb import extract_all_baseball_players_draft_info, \
    write_to_file_readable_for_computers
from src.models.PlayerDraft import PlayerDraft


class TestExtractAllBaseballPlayersDraftInfo:
    @dataclass
    class Params:
        expected: Set
        expected_api_calls: List

    @dataclass
    class Fixture:
        mock_stats_api: Mock
        actual: Set
        expected: Set
        expected_api_calls: List

    @pytest.fixture(
        ids=['Dynamic List, no filter'],
        params=[
            Params(
                expected={PlayerDraft(
                    id=123,
                    full_name='Bo',
                    college='fsu'
                )},
                expected_api_calls=[
                    call('draft', params={'year': '2000'}),
                    call('draft', params={'year': '2001'}),
                    call('draft', params={'year': '2002'}),
                    call('draft', params={'year': '2003'}),
                    call('draft', params={'year': '2004'}),
                    call('draft', params={'year': '2005'}),
                    call('draft', params={'year': '2006'}),
                    call('draft', params={'year': '2007'}),
                    call('draft', params={'year': '2008'}),
                    call('draft', params={'year': '2009'}),
                    call('draft', params={'year': '2010'}),
                    call('draft', params={'year': '2011'}),
                    call('draft', params={'year': '2012'}),
                    call('draft', params={'year': '2013'}),
                    call('draft', params={'year': '2014'}),
                    call('draft', params={'year': '2015'}),
                    call('draft', params={'year': '2016'}),
                    call('draft', params={'year': '2017'}),
                    call('draft', params={'year': '2018'}),
                    call('draft', params={'year': '2019'})
                ]
            )
        ])
    @patch('src.college.mlb.statsapi')
    def setup(self, mock_stats_api, request):
        mock_stats_api.get.return_value = {
            'drafts': {
                'rounds': [
                    {
                        'picks': [
                            {
                                'school': {'name': 'fsu'},
                                'person': {
                                    'id': 123,
                                    'fullName': 'Bo'
                                }
                            }
                        ]
                    }
                ]
            }
        }
        return TestExtractAllBaseballPlayersDraftInfo.Fixture(
            mock_stats_api=mock_stats_api,
            actual=extract_all_baseball_players_draft_info(),
            expected=request.param.expected,
            expected_api_calls=request.param.expected_api_calls
        )

    def test_stats_api_called(self, setup: Fixture):
        setup.mock_stats_api.get.assert_has_calls(setup.expected_api_calls)

    def test_output_correct(self, setup: Fixture):
        assert setup.actual == setup.expected


class TestWriteToFileReadableForComputers:
    @dataclass
    class Fixture:
        mock_baseball_players: Mock
        mock_open_file: Mock

    @pytest.fixture
    @patch('builtins.open', new_callable=mock_open())
    @patch('src.college.mlb.extract_all_baseball_players_draft_info')
    def setup(self, mock_baseball_players, mock_open_file):
        mock_open_file.reset_mock()
        mock_baseball_players.return_value = {
            PlayerDraft(id=1, full_name='Bo', college='fsu')
        }
        write_to_file_readable_for_computers()
        return TestWriteToFileReadableForComputers.Fixture(
            mock_baseball_players=mock_baseball_players,
            mock_open_file=mock_open_file
        )

    def test_extract_all_baseball_players_draft_info_called(self, setup: Fixture):
        setup.mock_baseball_players.assert_called_once()

    def test_open_file_called(self, setup: Fixture):
        setup.mock_open_file.assert_called_once_with('MLBPlayerDraft.json', 'w')

    def test_file_write_called(self, setup: Fixture):
        setup.mock_open_file.return_value.__enter__().write.assert_called_once_with(
            '{"1": {"id": 1, "college": "fsu"}}'
        )
