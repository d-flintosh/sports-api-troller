from src.api.golf_sport_radar import GolfSportRadar
from src.api.sport_radar import SportRadarApi

LPGA_BASE_URL = 'golf/trial/lpga/v3/en/2022' # Do we want/need to hardcode season year?


class LpgaSportRadar(GolfSportRadar):
    def __init__(self, api_client: SportRadarApi):
        super().__init__(api_client, LPGA_BASE_URL)
