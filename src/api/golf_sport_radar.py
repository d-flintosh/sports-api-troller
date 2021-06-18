from datetime import date
from abc import ABC
from typing import List

from src.api.sport_radar import SportRadarApi, BASE_URL
from src.models.PlayerDraft import PlayerDraft


class GolfSportRadar(ABC):
    def __init__(self, api_client: SportRadarApi, league_base_url: str):
        self.api_client = api_client
        self.league_base_url = league_base_url
    
    def get_tournament_schedule(self):
        SCHEUDLE_URL = '/tournaments/schedule.json'
        FULL_URL = BASE_URL + self.league_base_url + SCHEUDLE_URL
        return self.api_client.make_request(url=FULL_URL)

    def get_tournament_leaderboard(self, tournament_id: str):
        GAME_URL = f'/tournaments/{tournament_id}/leaderboard.json'
        FULL_URL = BASE_URL + self.league_base_url + GAME_URL
        return self.api_client.make_request(url=FULL_URL)

    def get_all_players_with_college(self) -> List[PlayerDraft]:
        players = []

        players_url = f'/players/profiles.json'
        full_url = BASE_URL + self.league_base_url + players_url
        response = self.api_client.make_request(url=full_url)

        for player in response.get('players'):
            players.append(
                PlayerDraft(
                    id=player.get('id'),
                    full_name=player.get('first_name') + ' ' + player.get('last_name'),
                    college=player.get('college')
                )
            )

        return players