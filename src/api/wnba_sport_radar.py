from src.api.basketball_sport_radar import BasketballSportRadar
from src.api.sport_radar import SportRadarApi

WNBA_BASE_URL = 'wnba/trial/v7/en/'


class WnbaSportRadar(BasketballSportRadar):
    def __init__(self, api_client: SportRadarApi):
        super().__init__(api_client, WNBA_BASE_URL)
