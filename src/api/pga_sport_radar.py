from src.api.golf_sport_radar import GolfSportRadar
from src.api.sport_radar import SportRadarApi

PGA_BASE_URL = 'golf/trial/pga/v3/en/2022' # Do we want/need to hardcode season year?


class PgaSportRadar(GolfSportRadar):
    def __init__(self, api_client: SportRadarApi):
        super().__init__(api_client, PGA_BASE_URL)
