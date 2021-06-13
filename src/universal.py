from google.cloud import pubsub_v1


def publish_message(message: str, school: str, send_message: bool = True):
    print(f'Publishing message: {message} for school: {school}')

    if send_message:
        publisher = pubsub_v1.PublisherClient()
        topic_id = 'projects/sports-data-service/topics/twitter-message-service-pubsub'
        future = publisher.publish(topic_id, str.encode(message), school=school)
        future.result()


def get_team_text(team_map: dict, team_id: int):
    team_text = ''
    if team_id:
        team = team_map.get(str(team_id), None)
        if team:
            twitter_code = team.get("twitterCode")
            if twitter_code:
                team_text = f' ({twitter_code})'

    return team_text
