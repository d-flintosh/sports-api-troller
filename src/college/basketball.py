from typing import Set

from nba_api.stats.endpoints import drafthistory
from nba_api.stats.library.parameters import LeagueID

from src.gcp.gcs import Gcs
from src.models.PlayerDraft import PlayerDraft


def extract_all_basketball_players_draft_info(league_id: LeagueID) -> Set[PlayerDraft]:
    draft_history = drafthistory.DraftHistory(league_id=league_id)

    players_to_return = []
    for key, players in draft_history.get_normalized_dict().items():
        for player in players:
            players_to_return.append(PlayerDraft(
                id=player.get('PERSON_ID'),
                full_name=player.get('PLAYER_NAME'),
                college=player.get('ORGANIZATION')
            ))
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
