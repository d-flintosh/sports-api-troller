import dataclasses
from dataclasses import dataclass
from functools import lru_cache
from operator import itemgetter
from typing import List, Optional

import requests
from bs4 import BeautifulSoup, ResultSet, Tag
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from src.gcp.gcs import Gcs


@dataclass
class PlayerObject:
    team_city: str
    team_name: str
    first_name: str
    last_name: str
    position: str
    year: str


@dataclass
class PlayerList:
    players: List[PlayerObject]


@dataclass
class RawPlayerObject:
    first_name: str
    last_name: str
    position: str
    year: str


@dataclass
class TeamDepthChart:
    team_city: str
    team_name: str
    depth_chart: ResultSet


@lru_cache(maxsize=None)
def make_api_call(url: str) -> BeautifulSoup:
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)
    response = http.get(url)
    return BeautifulSoup(response.text)


BASE_URL = 'https://www.ourlads.com/ncaa-football-depth-charts/'


def get_all_depth_chart_urls() -> List[str]:
    urls = []
    soup = make_api_call(url=BASE_URL)
    for team_row in soup.find_all('div', {'class': 'nfl-dc-mm-team-links'}):
        for depth_chart_row in team_row.find_all('a'):
            if depth_chart_row.get_text().strip().lower() == 'depth chart':
                urls.append(depth_chart_row.get('href'))

    return urls


def get_depth_chart_by_team(team_url: str) -> Optional[TeamDepthChart]:
    soup = make_api_call(url=f'{BASE_URL}{team_url}')
    team_city = soup.find('span', {'class': 'pt-team-city'}).get_text().strip()
    team_name = soup.find('span', {'class': 'pt-team-name'}).get_text().strip()
    if team_city != 'FCS & Small College NFL Prospects':
        player_table = soup.find('table', {'class': 'table table-bordered'})
        return TeamDepthChart(
            team_city=team_city,
            team_name=team_name,
            depth_chart=player_table.find_all('tr', {'class': ['row-dc-wht', 'row-dc-grey']})
        )
    return None


def do_things():
    depth_chart_urls = get_all_depth_chart_urls()
    players = []
    for depth_chart_url in depth_chart_urls:
        team = get_depth_chart_by_team(team_url=depth_chart_url)
        if team:
            for depth_chart_record in team.depth_chart:
                raw_player_records = convert_depth_chart_record(
                    record=depth_chart_record
                )

                for player in raw_player_records:
                    players.append(
                        PlayerObject(
                            position=player.position,
                            first_name=player.first_name,
                            last_name=player.last_name,
                            year=player.year,
                            team_city=team.team_city,
                            team_name=team.team_name
                        )
                    )

    if players:
        Gcs(bucket='college-by-player').write(
            url='cfb/players.json',
            contents=dataclasses.asdict(PlayerList(players=players))
        )


def convert_fields_to_raw_player(fields: ResultSet, start_index: int) -> Optional[RawPlayerObject]:
    position = fields[0].get_text().strip()
    name = fields[start_index].get_text().strip()
    name_parts = name.split(',')
    if len(name_parts) == 0 or name_parts[0].strip() == '':
        return None
    year_parts = name_parts[1].split(' ')
    if len(year_parts) > 3:
        year_text = ' '.join(itemgetter(2, len(year_parts) - 1)(year_parts)).strip()
    else:
        year_text = year_parts[2]
    return RawPlayerObject(
        position=position,
        first_name=year_parts[1].strip(),
        last_name=name_parts[0],
        year=year_text
    )


def convert_depth_chart_record(record: ResultSet) -> List[RawPlayerObject]:
    players = []
    fields = record.find_all('td')
    for i in range(1, 4):
        player = convert_fields_to_raw_player(fields=fields, start_index=i * 2)
        if player:
            players.append(player)
    return players
