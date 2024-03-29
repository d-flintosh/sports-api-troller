from src.gcp.gcs import Gcs
from src.models.PlayerDraft import PlayerDraft


def write_to_file_readable_for_computers(league: str, league_client):
    players: [PlayerDraft] = league_client.get_all_players_with_college()
    output = {}
    for player in players:
        output[player.id] = {
            'id': player.id,
            'full_name': player.full_name,
            'college': player.college
        }
    Gcs(bucket='college-by-player').write(url=f'{league}/players.json', contents=output)

