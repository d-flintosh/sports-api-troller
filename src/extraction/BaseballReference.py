import requests
from bs4 import BeautifulSoup, Tag, Comment
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from src.gcp.gcs import Gcs
from src.historical import historical_stats_bucket


def get_mlb_all_time_leaders(team: dict):
    team_id = team.get('mlb_reference')
    url = f'https://www.baseball-reference.com/schools/?key_school={team_id}'
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
    for row in soup.find('table', id='school_batting').tbody:
        if isinstance(row, Tag):
            try:
                players.append({
                    'full_name': find_stat_by_name(row, 'player').contents[0],
                    'hits': int(find_stat_by_name(row, 'H')),
                    'home_runs': int(find_stat_by_name(row, 'HR')),
                    'stolen_bases': int(find_stat_by_name(row, 'SB')),
                    'rbis': int(find_stat_by_name(row, 'RBI'))
                })
            except IndexError as e:
                print(e)

    comments = soup.find(text=lambda text: isinstance(text, Comment) and 'id="school_pitching"' in text)
    soup_pitching = BeautifulSoup(comments)
    for row in soup_pitching.find('table', id='school_pitching').tbody:
        if isinstance(row, Tag):
            full_name = find_stat_by_name(row, 'player').contents[0]
            try:
                if not any(player.get('full_name') == full_name for player in players):
                    players.append({
                        'full_name': full_name,
                        'pitching_strikeouts': int(find_stat_by_name(row, 'SO')),
                        'pitching_wins': int(find_stat_by_name(row, 'W')),
                        'pitching_saves': int(find_stat_by_name(row, 'SV'))
                    })
                else:
                    player = next(filter(lambda player: player.get('full_name') == full_name, players))
                    player['pitching_strikeouts'] = int(find_stat_by_name(row, 'SO'))
                    player['pitching_wins'] = int(find_stat_by_name(row, 'W'))
                    player['pitching_saves'] = int(find_stat_by_name(row, 'SV'))

            except IndexError as e:
                print(e)

    player_stats = {
        'player_stats': players
    }
    school = team.get('in_the_pros')
    full_path = f'mlb/{school}/all_players/players.json'
    gcs = Gcs(bucket=historical_stats_bucket)
    gcs.write(url=full_path, contents=player_stats)


def find_stat_by_name(row: Tag, stat_name: str):
    return row.find('td', attrs={'data-stat': stat_name}).contents[0]
