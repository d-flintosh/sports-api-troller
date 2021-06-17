from datetime import date
from abc import ABC
from typing import List

from src.api.sport_radar import SportRadarApi, BASE_URL
from src.models.PlayerDraft import PlayerDraft


class BasketballSportRadar(ABC):
    def __init__(self, api_client: SportRadarApi, league_base_url: str):
        self.api_client = api_client
        self.league_base_url = league_base_url

    def get_daily_schedule(self, date: date):
        SCHEUDLE_URL = f'games/{date.year}/{str(date.month).zfill(2)}/{str(date.day).zfill(2)}/schedule.json'
        FULL_URL = BASE_URL + self.league_base_url + SCHEUDLE_URL
        return self.api_client.make_request(url=FULL_URL)

    def get_boxscore(self, game_id: str):
        GAME_URL = f'games/{game_id}/summary.json'
        FULL_URL = BASE_URL + self.league_base_url + GAME_URL
        return self.api_client.make_request(url=FULL_URL)

    def get_all_team_ids(self) -> List[str]:
        TEAMS_URL = 'league/hierarchy.json'
        FULL_URL = BASE_URL + self.league_base_url + TEAMS_URL
        response = self.api_client.make_request(url=FULL_URL)

        team_ids = []

        for conference in response.get('conferences'):
            for division in conference.get('divisions', [{'teams': conference.get('teams')}]):
                for team in division.get('teams'):
                    team_ids.append(team.get('id'))
        return team_ids

    def get_all_players_with_college(self) -> List[PlayerDraft]:
        team_ids = self.get_all_team_ids()
        players = []

        for team in team_ids:
            roster_url = f'teams/{team}/profile.json'
            full_url = BASE_URL + self.league_base_url + roster_url
            response = self.api_client.make_request(url=full_url)

            for player in response.get('players'):
                players.append(
                    PlayerDraft(
                        id=player.get('id'),
                        full_name=player.get('full_name'),
                        college=player.get('college')
                    )
                )

        return players
