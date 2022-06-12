from datetime import date, datetime
from typing import List

from dateutil import tz

from src.api.sport_radar import SportRadarApi, BASE_URL
from src.models.PlayerDraft import PlayerDraft

NFL_BASE_URL = 'nfl/official/trial/v7/en/'


class NflSportRadar:
    def __init__(self, api_client: SportRadarApi):
        self.api_client = api_client

    def get_daily_schedule(self, date: date):
        SCHEUDLE_URL = f'games/2022/REG/schedule.json'
        FULL_URL = BASE_URL + NFL_BASE_URL + SCHEUDLE_URL

        full_schedule = self.api_client.make_request(url=FULL_URL)
        games = []
        for week in full_schedule.get('weeks', []):
            for game in week.get('games', []):
                game_date = datetime.fromisoformat(game.get('scheduled')).replace(
                    tzinfo=tz.gettz('UTC')
                )
                game_date = game_date.astimezone(tz.gettz('America/Chicago'))
                if game_date.date() == date:
                    games.append(game)
        return games

    def get_boxscore(self, game_id: str):
        GAME_URL = f'games/{game_id}/statistics.json'
        FULL_URL = BASE_URL + NFL_BASE_URL + GAME_URL
        return self.api_client.make_request(url=FULL_URL)

    def get_all_team_ids(self) -> List[str]:
        TEAMS_URL = 'league/hierarchy.json'
        FULL_URL = BASE_URL + NFL_BASE_URL + TEAMS_URL
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
            full_url = BASE_URL + NFL_BASE_URL + roster_url
            response = self.api_client.make_request(url=full_url)

            for player in response.get('players'):
                players.append(
                    PlayerDraft(
                        id=player.get('id'),
                        full_name=player.get('name'),
                        college=player.get('college')
                    )
                )

        return players
