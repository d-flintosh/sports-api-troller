from google.cloud import pubsub_v1

from src.models.Schools import fsu_school_names


def is_fsu(school: str):
    if school and school and any(list(map(lambda x: x == school.lower(), fsu_school_names))):
        return True
    return False


def publish_message(message: str, school: str, send_message: bool = True):
    print(f'Publishing message: {message} for school: {school}')

    if send_message:
        publisher = pubsub_v1.PublisherClient()
        topic_id = 'projects/sports-data-service/topics/twitter-message-service-pubsub'
        future = publisher.publish(topic_id, str.encode(message), school=school)
        future.result()