import json
from typing import Callable, Set

import statsapi

from src.models.PlayerDraft import PlayerDraft
from src.universal import is_fsu

mlb_fsu_player_ids = {424706, 461881, 449142, 460368, 453625, 424366, 453625, 451795, 461749, 453461, 458245, 455072,
                      458233, 451795, 444360, 458244, 451196, 456650, 452220, 452245, 453593, 453561, 446564, 489075,
                      488778, 446135, 453203, 502086, 446135, 502228, 506917, 446273, 506912, 450572, 446344, 506925,
                      506927, 506914, 457763, 475424, 446344, 506927, 506918, 534631, 502076, 502219, 502781, 457748,
                      518713, 534630, 534627, 506924, 518642, 519010, 543219, 519010, 607257, 581639, 607256, 518642,
                      607256, 581532, 581530, 622212, 581527, 582473, 543747, 572879, 643440, 595328, 592247, 642006,
                      643260, 643540, 596133, 605335, 595328, 572879, 595895, 657763, 596056, 621466, 641507, 650327,
                      650393, 664928, 605282, 605208, 623518, 670764, 656275, 676811, 656586, 656290, 641429, 656604,
                      663947, 650397, 663728, 663485, 656604, 663622, 663947, 680501, 656586, 666141, 669001, 669283,
                      663682}


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


def get_fsu_baseball_players(use_static_list: bool) -> Set:
    if use_static_list:
        return mlb_fsu_player_ids

    return set(map(lambda x: x.id, extract_all_baseball_players_draft_info()))
