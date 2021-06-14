import time
from typing import Set

from nba_api.stats.endpoints import commonallplayers, commonplayerinfo
from nba_api.stats.library.parameters import LeagueID

from src.gcp.gcs import Gcs
from src.models.PlayerDraft import PlayerDraft


def extract_all_basketball_players_draft_info(league_id: LeagueID) -> Set[PlayerDraft]:
    all_players = commonallplayers.CommonAllPlayers(
        is_only_current_season=1,
        league_id=league_id
    ).get_normalized_dict().get('CommonAllPlayers')

    players_to_return = []
    for player in all_players:
        try:
            player_info = commonplayerinfo.CommonPlayerInfo(player_id=player.get('PERSON_ID'))\
                .get_normalized_dict().get('CommonPlayerInfo')[0]
            players_to_return.append(PlayerDraft(
                id=player_info.get('PERSON_ID'),
                full_name=player_info.get('DISPLAY_FIRST_LAST'),
                college=player_info.get('SCHOOL')
            ))
        except:
            print(f'Failed for player {player}')

        time.sleep(2)

    return set(players_to_return)


def write_to_file_readable_for_computers(league_id: LeagueID):
    players: {PlayerDraft} = extract_all_basketball_players_draft_info(league_id=league_id)
    output = {}
    for player in players:
        output[player.id] = {
            'id': player.id,
            'college': player.college
        }
    league_id_string = convert_league_id_to_string(league_id)
    Gcs().write(url=f'{league_id_string}/players.json', contents=output)


def convert_league_id_to_string(league_id: LeagueID):
    return 'nba' if league_id == LeagueID.nba else 'wnba'
