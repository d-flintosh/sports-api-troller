import pandas
import statsapi

from src.gcp.gcs import Gcs


def get_stuff(start_date: str, end_date: str):
    gcs = Gcs(bucket='event-stats-raw')
    date_range = pandas.date_range(start=start_date, end=end_date)
    for date in date_range:
        formatted_date = date.strftime("%m/%d/%Y")
        print(f'Getting games played for date: {formatted_date}')
        try:
            schedule = statsapi.schedule(date=formatted_date)
            print(schedule)
            for game in schedule:
                game_id = game.get('game_id')
                print(game_id)
                boxscore = statsapi.boxscore_data(gamePk=game_id)

                gcs.write(url=f'mlb/{game_id}.json', contents=boxscore)
        except Exception as e:
            print(f'Date Failed: {formatted_date}')
