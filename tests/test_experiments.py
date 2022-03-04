from datetime import date, datetime

import pytest
from nba_api.stats.library.parameters import LeagueID

from src.api.basketball_nba_api import BasketballNbaApi
from src.api.lpga_sport_radar import LpgaSportRadar
from src.api.mlb_sport_radar import MlbSportRadar
from src.api.nba_sport_radar import NbaSportRadar
from src.api.nfl_sport_radar import NflSportRadar
from src.api.nhl_sport_radar import NhlSportRadar
from src.api.pga_sport_radar import PgaSportRadar
from src.api.sport_radar import SportRadarApi
from src.api.wnba_sport_radar import WnbaSportRadar
from src.college.write_players_to_gcs import write_to_file_readable_for_computers
from src.extraction.BaseballLeague import BaseballLeague
from src.extraction.BaseballReference import get_mlb_all_time_leaders
from src.extraction.BasketballLeague import BasketballLeague
from src.extraction.HockeyLeague import HockeyLeague
from src.extraction.HockeyReference import get_nhl_all_time_leaders
from src.historical.basketball_significance import basketball_stat_list
from src.historical.mlb_significance import mlb_stat_list
from src.historical.nhl_significance import nhl_stat_list
from src.historical.significance import get_top_3_players_by_stat
from src.models.BasketballStatPlayer import BasketballStatPlayer
from src.models.Schools import nba_api_college_names, nhl_reference_college_names, mlb_reference_college_names
from src.models.SendTweetForSchool import SendTweetForSchool
from src.tweet_driver import tweet_driver
from src.universal import publish_message


@pytest.mark.skip(reason="only run this manually")
def test_daily():
    api_client = SportRadarApi()
    leagues = [
        BasketballLeague(league_name='nba', league_client=NbaSportRadar(api_client=api_client))
    ]
    tweet_driver(
        leagues=leagues,
        date_to_run=date(2022, 2, 28),
        send_message=False,
        skip_filter=True
    )


@pytest.mark.skip(reason="only run this manually")
def test_hourly():
    api_client = SportRadarApi()
    leagues = [
        BaseballLeague(league_client=MlbSportRadar(api_client=api_client)),
        BasketballLeague(league_name='nba', league_client=NbaSportRadar(api_client=api_client)),
        BasketballLeague(league_name='wnba', league_client=WnbaSportRadar(api_client=api_client)),
        HockeyLeague(league_name='nhl', league_client=NhlSportRadar(api_client=api_client)),
    ]
    tweet_driver(
        leagues=leagues,
        date_to_run=date(2021, 7, 16),
        send_message=False,
        skip_filter=False
    )


@pytest.mark.skip(reason="only run this manually")
def test_extract_baseball_draft_info():
    api_client = SportRadarApi()
    mlb_client = MlbSportRadar(api_client=api_client)
    write_to_file_readable_for_computers(league='mlb', league_client=mlb_client)


@pytest.mark.skip(reason="only run this manually")
def test_extract_basketball_draft_info():
    api_client = SportRadarApi()
    nba_client = NbaSportRadar(api_client=api_client)
    wnba_client = WnbaSportRadar(api_client=api_client)
    write_to_file_readable_for_computers(league='nba', league_client=nba_client)
    write_to_file_readable_for_computers(league='wnba', league_client=wnba_client)


@pytest.mark.skip(reason="only run this manually")
def test_extract_nhl_draft_info():
    api_client = SportRadarApi()
    nhl_client = NhlSportRadar(api_client=api_client)
    write_to_file_readable_for_computers(league='nhl', league_client=nhl_client)


@pytest.mark.skip(reason="only run this manually")
def test_extract_golf_draft_info():
    api_client = SportRadarApi()
    pga_client = PgaSportRadar(api_client=api_client)
    lpga_client = LpgaSportRadar(api_client=api_client)
    write_to_file_readable_for_computers(league='pga', league_client=pga_client)
    write_to_file_readable_for_computers(league='lpga', league_client=lpga_client)


@pytest.mark.skip(reason="only run this manually")
def test_extract_nfl_draft_info():
    api_client = SportRadarApi()
    nfl_client = NflSportRadar(api_client=api_client)
    write_to_file_readable_for_computers(league='nfl', league_client=nfl_client)


@pytest.mark.skip(reason="only run this manually")
def test_get_player_by_college_stats():
    nba_api = BasketballNbaApi(league_name='nba', league_id=LeagueID.nba)
    wnba_api = BasketballNbaApi(league_name='wnba', league_id=LeagueID.wnba)

    for college in nba_api_college_names:
        nba_api.save_player_by_college(college=college)
        wnba_api.save_player_by_college(college=college)


@pytest.mark.skip(reason="only run this manually")
def test_nhl_hockey_reference():
    for team in nhl_reference_college_names:
        get_nhl_all_time_leaders(team=team)


@pytest.mark.skip(reason="only run this manually")
def test_mlb_hockey_reference():
    for team in mlb_reference_college_names:
        get_mlb_all_time_leaders(team=team)


@pytest.mark.skip(reason="only run this manually")
def test_get_nba_career_stats():
    for college in nba_api_college_names:
        for stat_key, stat_text in basketball_stat_list:
            top_3 = get_top_3_players_by_stat(
                school=college.get('in_the_pros'),
                league_name='nba',
                stat_key=stat_key,
                dictionary_key='PlayerCareerByCollege',
                player_name_key='PLAYER_NAME'
            )
            header_text = f'#NBA Leaders in {stat_text}\n\n'
            top_3_text = '\n'.join(top_3)
            publish_message(
                message=header_text + top_3_text,
                school=college.get('in_the_pros'),
                topic='twitter-message-service-pubsub',
                send_message=False
            )


@pytest.mark.skip(reason="only run this manually")
def test_get_nhl_career_stats():
    for college in nhl_reference_college_names:
        for stat_key, stat_text in nhl_stat_list:
            top_3 = get_top_3_players_by_stat(
                school=college.get('in_the_pros'),
                league_name='nhl',
                stat_key=stat_key,
                dictionary_key='player_stats',
                player_name_key='full_name'
            )
            header_text = f'#NHL Leaders in {stat_text}\n\n'
            top_3_text = '\n'.join(top_3)
            publish_message(
                message=header_text + top_3_text,
                school=college.get('in_the_pros'),
                topic='twitter-message-service-pubsub',
                send_message=False
            )


@pytest.mark.skip(reason="only run this manually")
def test_get_mlb_career_stats():
    for college in mlb_reference_college_names:
        for stat_key, stat_text in mlb_stat_list:
            top_3 = get_top_3_players_by_stat(
                school=college.get('in_the_pros'),
                league_name='mlb',
                stat_key=stat_key,
                dictionary_key='player_stats',
                player_name_key='full_name'
            )
            header_text = f'#MLB Leaders in {stat_text}\n\n'
            top_3_text = '\n'.join(top_3)
            publish_message(
                message=header_text + top_3_text,
                school=college.get('in_the_pros'),
                topic='twitter-message-service-pubsub',
                send_message=False
            )


@pytest.mark.skip(reason="only run this manually")
def test_commit_a_bunch_of_sins():
    api = BasketballNbaApi(league_name='nba', league_id=LeagueID.nba)
    test_college = [{
        'nba_api': 'Ohio State',
        'in_the_pros': 'ohiostate'
    }]
    for college in nba_api_college_names:
        # for college in test_college:
        tweetable_objects = []
        college_players = []
        player_ids = api.get_historical_player_ids_by_college(college=college)
        for player_id in player_ids:
            player = api.get_player_by_college(college=college, player_id=player_id)
            season_totals = player.get('SeasonTotalsRegularSeason')
            is_current_season = False
            current_season = '2021-22'
            if any(season.get('SEASON_ID') == current_season for season in season_totals):
                is_current_season = True
            player_subset = {
                'player_name': player.get('player_name'),
                'season_totals': season_totals,
                'career_highs': player.get('CareerHighs'),
                'season_highs': player.get('SeasonHighs'),
                'is_current_season': is_current_season
            }
            college_players.append(player_subset)

        current_college_players = list(filter(lambda x: x.get('is_current_season'), college_players))

        stats = [
            {
                'nba_api_text': 'PTS',
                'common_text': 'points'
            },
            {
                'nba_api_text': 'REB',
                'common_text': 'rebounds'
            },
            {
                'nba_api_text': 'AST',
                'common_text': 'assists'
            },
            {
                'nba_api_text': 'FG3M',
                'common_text': '3\'s'
            },
            {
                'nba_api_text': 'STL',
                'common_text': 'steals'
            },
            {
                'nba_api_text': 'BLK',
                'common_text': 'blocks'
            }
        ]

        for stat in stats:
            max_stat_by_player = {}
            for player in current_college_players:
                max_stat = list(filter(
                    lambda x: x.get('STAT') == stat.get('nba_api_text') and datetime.strptime(x.get('GAME_DATE'),
                                                                                              '%b %d %Y') >= datetime(
                        2021, 9, 1), player.get('season_highs')
                ))
                if max_stat:
                    max_stat = max_stat[0]
                    if max_stat.get('STAT_VALUE') > max_stat_by_player.get('the_stat', {}).get('STAT_VALUE', 0):
                        max_stat_by_player = player
                        max_stat_by_player['the_stat'] = max_stat

            max_career_stat_by_player = []
            for player in college_players:
                max_stat = list(filter(
                    lambda x: x.get('STAT') == stat.get('nba_api_text') and datetime.strptime(x.get('GAME_DATE'),
                                                                                              '%b %d %Y') < datetime(
                        2021, 9, 1), player.get('career_highs')
                ))
                if max_stat:
                    max_stat = max_stat[0]
                    if max_stat.get('STAT_VALUE') >= max_stat_by_player.get('the_stat', {}).get('STAT_VALUE', 0):
                        max_career = player
                        max_career['the_career_stat'] = max_stat
                        max_career_stat_by_player.append(max_career)
            try:
                most_recent_max_career_stat = max(max_career_stat_by_player, key=lambda x: datetime.strptime(
                    x.get('the_career_stat').get('GAME_DATE'), '%b %d %Y'))
            except ValueError as e:
                most_recent_max_career_stat = {}

            the_tweet = BasketballStatPlayer(
                college=college,
                stat_name=stat.get('common_text'),
                current_player_name=max_stat_by_player.get('player_name'),
                current_player_stat_value=max_stat_by_player.get('the_stat').get('STAT_VALUE'),
                previous_player_name=most_recent_max_career_stat.get('player_name', None),
                previous_player_stat_value=most_recent_max_career_stat.get('the_career_stat', {}).get('STAT_VALUE',
                                                                                                      None),
                previous_player_date=most_recent_max_career_stat.get('the_career_stat', {}).get('GAME_DATE', None)
            )
            tweetable_objects.append(the_tweet)
        SendTweetForSchool(
            school=college.get('in_the_pros'),
            player_stats=tweetable_objects,
            send_message=False
        ).publish(
            sport='basketball',
            league_name='nba'
        )
