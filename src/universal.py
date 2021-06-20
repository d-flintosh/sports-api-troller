from typing import Union, List

from google.api_core.exceptions import NotFound
from google.cloud import pubsub_v1

from src.gcp.gcs import Gcs


def publish_message(message: str, school: str, send_message: bool = True):
    print(f'Publishing message: {message} for school: {school}')

    if send_message:
        publisher = pubsub_v1.PublisherClient()
        topic_id = 'projects/sports-data-service/topics/twitter-message-service-pubsub'
        future = publisher.publish(topic_id, str.encode(message), school=school)
        future.result()


def get_previously_published_games(league_name: str, date) -> List:
    formatted_date = date.strftime('%Y-%m-%d')
    try:
        games_published = Gcs(bucket='tweet-checkpoints').read_as_dict(url=f'{league_name}/{formatted_date}.json')
    except NotFound as e:
        games_published = {}

    return games_published.get('games_published', [])


def update_tweet_checkpoint(league_name: str, send_message: bool, date, games_published: List):
    if send_message and games_published:
        formatted_date = date.strftime('%Y-%m-%d')
        contents = {
            'games_published': games_published
        }
        Gcs(bucket='tweet-checkpoints').write(url=f'{league_name}/{formatted_date}.json', contents=contents)


def get_team_text(team_map: dict, team_id: Union[str, int]):
    team_text = ''
    if team_id:
        team = team_map.get(str(team_id), None)
        if team:
            twitter_code = team.get("twitterCode")
            if twitter_code:
                team_text = f' ({twitter_code})'

    return team_text
