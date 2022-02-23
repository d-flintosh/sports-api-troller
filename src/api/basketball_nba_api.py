import time
from typing import List

from nba_api.stats.endpoints import playercareerbycollege, playerprofilev2
from nba_api.stats.library.parameters import LeagueID

from src.gcp.gcs import Gcs


class BasketballNbaApi:
    def __init__(self, league_name: str, league_id: LeagueID):
        self.league_id = league_id
        self.league_name = league_name
        self.gcs_path_college_by_player_stats = 'college-by-player-stats'
        self.gcs = Gcs(bucket=self.gcs_path_college_by_player_stats)

    def save_player_by_college(self, college: dict) -> None:
        try:
            player_info = playercareerbycollege.PlayerCareerByCollege(
                college=college.get('nba_api'),
                league_id=self.league_id
            )
            player_dict = player_info.get_normalized_dict()
            self.gcs.write(
                url=f'{self.league_name}/{college.get("in_the_pros")}/all_players/players.json',
                contents=player_dict
            )
            for player in player_dict.get('PlayerCareerByCollege'):
                time.sleep(.5)
                player_id = player.get('PLAYER_ID')
                player_name = player.get('PLAYER_NAME')
                player_profile = playerprofilev2.PlayerProfileV2(
                    player_id=player_id, league_id_nullable=self.league_id
                )
                player_profile_dict = player_profile.get_normalized_dict()
                player_profile_dict['player_name'] = player_name
                self.gcs.write(
                    url=f'{self.league_name}/{college.get("in_the_pros")}/player/{player_id}.json',
                    contents=player_profile_dict
                )
        except Exception as e:
            print(f'Failed for college: {college}')

    def get_historical_player_ids_by_college(self, college: dict) -> List[str]:
        prefix = f'{self.league_name}/{college.get("in_the_pros")}/all_players/players.json'
        all_players = self.gcs.read_as_dict(url=prefix)
        return list(map(lambda x: x.get('PLAYER_ID'), all_players.get('PlayerCareerByCollege')))

    def get_player_by_college(self, college: dict, player_id: str):
        prefix = f'{self.league_name}/{college.get("in_the_pros")}/player/{player_id}.json'
        player = self.gcs.read_as_dict(url=prefix)
        return player

