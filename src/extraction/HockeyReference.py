import requests
from bs4 import BeautifulSoup, Tag
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from src.gcp.gcs import Gcs
from src.historical import historical_stats_bucket


def get_nhl_all_time_leaders(team: dict):
    team_id = team.get('nhl_reference')
    url = f'https://www.hockey-reference.com/amateurs/team.cgi?t={team_id}'
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
    soup = BeautifulSoup(response.text)
    players = []
    for row in soup.tbody:
        if isinstance(row, Tag):
            players.append({
                'full_name': parse_name(row.th.a.contents[0]),
                'goals': find_stat_by_name(row, 'goals'),
                'assists': find_stat_by_name(row, 'assists')
            })

    player_stats = {
        'player_stats': players
    }
    school = team.get('in_the_pros')
    full_path = f'nhl/{school}/all_players/players.json'
    gcs = Gcs(bucket=historical_stats_bucket)
    gcs.write(url=full_path, contents=player_stats)


def find_stat_by_name(row: Tag, stat_name: str):
    return int(row.find('td', attrs={'data-stat': stat_name}).contents[0])


def parse_name(name: str) -> str:
    full_name = name.split(',')
    return f'{full_name[1].lstrip()} {full_name[0]}'
