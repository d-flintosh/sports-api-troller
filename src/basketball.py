import time

from nba_api.stats.endpoints import scoreboard, commonplayerinfo, boxscoretraditionalv2

from src.universal import is_fsu, publish_message


def get_basketball(date_to_run, league_id: str, send_message: bool):
    fsu_player_boxscores = []
    formatted_date = date_to_run.strftime('%m/%d/%Y')
    print(f'Getting games played for date: {formatted_date}')
    schedule = scoreboard.Scoreboard(game_date=formatted_date, league_id=league_id)
    game_ids = set(map(lambda x: x.get('GAME_ID'), schedule.get_normalized_dict().get('GameHeader')))

    for game_id in game_ids:
        boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)

        for player in boxscore.get_normalized_dict().get('PlayerStats'):
            time.sleep(2)
            player_id = player.get('PLAYER_ID')
            player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id).get_normalized_dict()
            if any(list(map(lambda x: is_fsu(x.get('SCHOOL')), player_info.get('CommonPlayerInfo')))):
                fsu_player_boxscores.append(player)

    tweet_message = ''
    should_publish_message = False

    for fsu_player in fsu_player_boxscores:
        stat_line = []
        player_points = fsu_player.get('PTS', 0)
        player_rebounds = fsu_player.get('REB', 0)
        player_assists = fsu_player.get('AST', 0)
        if player_points or player_rebounds or player_assists:
            if player_points and player_points > 0:
                stat_line.append(f'{player_points} pts')
            if player_rebounds and player_rebounds > 0:
                stat_line.append(f'{player_rebounds} reb')
            if player_assists and player_assists > 0:
                stat_line.append(f'{player_assists} ast')

            if stat_line:
                should_publish_message = True

            tweet_message = tweet_message + f'{fsu_player.get("PLAYER_NAME")} {"/".join(stat_line)}'

    if should_publish_message:
        publish_message(message=tweet_message, send_message=send_message, school='fsu')
