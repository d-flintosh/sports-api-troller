import json
from typing import Set

import statsapi

from src.models.PlayerDraft import PlayerDraft


def has_required_fields(player: dict) -> bool:
    if not player.get('school'):
        return False

    if not player.get('school').get('name'):
        return False

    if not player.get('person'):
        return False

    if not player.get('person').get('id'):
        return False

    if not player.get('person').get('fullName'):
        return False

    return True


def extract_all_baseball_players_draft_info() -> Set[PlayerDraft]:
    output: [PlayerDraft] = []
    for year in range(2000, 2020):
        params = {
            'year': str(year)
        }
        print(f'Making Draft Call for the Year {year}')
        draft = statsapi.get('draft', params=params)

        for round in draft.get('drafts').get('rounds'):
            for pick in round.get('picks'):
                if has_required_fields(player=pick):
                    output.append(PlayerDraft(
                        id=pick.get('person').get('id'),
                        full_name=pick.get('person').get('fullName'),
                        college=pick.get('school').get('name')
                    ))
    return set(output)


def write_to_file_readable_for_computers():
    players: {PlayerDraft} = extract_all_baseball_players_draft_info()
    output = {}
    for player in players:
        output[player.id] = {
            'id': player.id,
            'college': player.college
        }

    with open('MLBPlayerDraft.json', 'w') as file:
        file.write(json.dumps(output))
