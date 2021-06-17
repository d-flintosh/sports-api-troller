from src.api.basketball_sport_radar import BasketballSportRadar
from src.gcp.gcs import Gcs
from src.models.PlayerDraft import PlayerDraft


def write_to_file_readable_for_computers(league: str, league_client: BasketballSportRadar):
    players: [PlayerDraft] = league_client.get_all_players_with_college()
    output = {}
    for player in players:
        output[player.id] = {
            'id': player.id,
            'college': player.college
        }
    Gcs(bucket='college-by-player').write(url=f'{league}/players.json', contents=output)

