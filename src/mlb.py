def get_mlb(date_to_run) -> MessageObject:
    player_ids_to_check = get_fsu_baseball_players(use_static_list=True)
    fsu_player_boxscores = []
    formatted_date = date_to_run.strftime('%m/%d/%Y')
    print(f'Getting games played for date: {formatted_date}')
    schedule = statsapi.schedule(date=formatted_date)
    for game in schedule:
        boxscore = statsapi.boxscore_data(gamePk=game.get('game_id'))
        fsu_player_boxscores = fsu_player_boxscores + player_stats_iterator(team=boxscore.get('away'),
                                                                            player_ids=player_ids_to_check)
        fsu_player_boxscores = fsu_player_boxscores + player_stats_iterator(team=boxscore.get('home'),
                                                                            player_ids=player_ids_to_check)
    tweet_message = ''
    for fsu_player in fsu_player_boxscores:
        tweet_message = tweet_message + f'{fsu_player.get("person").get("fullName")} went {fsu_player.get("stats").get("batting").get("hits")}-{fsu_player.get("stats").get("batting").get("atBats")}. '

    if fsu_player_boxscores:
        publish_message(message=tweet_message)

    return MessageObject(raw_data=fsu_player_boxscores, message=tweet_message)