from google.cloud import pubsub_v1


def is_fsu(school: str):
    _fsu = ['florida state', 'fsu', 'florida state university']

    if school and school and any(list(map(lambda x: x == school.lower(), _fsu))):
        return True
    return False


def publish_message(message: str):
    publisher = pubsub_v1.PublisherClient()
    topic_id = 'projects/sports-data-service/topics/twitter-message-service-pubsub'
    print(f'Publishing message: {message}')
    future = publisher.publish(topic_id, str.encode(message))
    future.result()