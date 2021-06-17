from src.api.basketball_sport_radar import BasketballSportRadar
from src.api.sport_radar import SportRadarApi

NBA_BASE_URL = 'nba/trial/v7/en/'


class NbaSportRadar(BasketballSportRadar):
    def __init__(self, api_client: SportRadarApi):
        super().__init__(api_client, NBA_BASE_URL)
