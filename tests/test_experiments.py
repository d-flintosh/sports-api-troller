from datetime import date

import pytest
import statsapi
from nba_api.stats.endpoints import commonallplayers, commonplayerinfo
from nba_api.stats.library.parameters import LeagueID

from src.basketball import get_basketball
from src.college.basketball import write_to_file_readable_for_computers
from src.mlb import get_mlb


@pytest.mark.skip(reason="only run this manually")
def test_mlb():
    get_mlb(date(2021, 6, 13), send_message=False)


@pytest.mark.skip(reason="only run this manually")
def test_get_basketball():
    get_basketball(date(2021, 6, 13), send_message=False, league_id=LeagueID.nba)


@pytest.mark.skip(reason="only run this manually")
def test_get_mlb_teams_from_api():
    print(statsapi.lookup_team(''))


@pytest.mark.skip(reason="only run this manually")
def test_get_basketball_players_from_api():
    print(commonallplayers.CommonAllPlayers(
        is_only_current_season=1,
        league_id=LeagueID.wnba
    ).get_normalized_dict())


@pytest.mark.skip(reason="only run this manually")
def test_get_basketball_teams_from_api():
    all_players = commonallplayers.CommonAllPlayers(
        is_only_current_season=1,
        league_id=LeagueID.wnba
    ).get_normalized_dict().get('CommonAllPlayers')

    team_map = {}
    for player in all_players:
        team_map[str(player.get('TEAM_ID'))] = {
            'id': player.get('TEAM_ID'),
            'teamCode': player.get('TEAM_ABBREVIATION')
        }

    print(team_map)


@pytest.mark.skip(reason="only run this manually")
def test_get_basketball_player_from_api():
    player_info = commonplayerinfo.CommonPlayerInfo(player_id=1630172).get_normalized_dict().get('CommonPlayerInfo')[0]
    print(player_info)


@pytest.mark.skip(reason="only run this manually")
def test_extract_basketball_draft_info():
    print(write_to_file_readable_for_computers(league_id=LeagueID.nba))
    print(write_to_file_readable_for_computers(league_id=LeagueID.wnba))