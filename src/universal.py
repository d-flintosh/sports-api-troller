from google.cloud import pubsub_v1


def publish_message(message: str, school: str, send_message: bool = True):
    print(f'Publishing message: {message} for school: {school}')

    if send_message:
        publisher = pubsub_v1.PublisherClient()
        topic_id = 'projects/sports-data-service/topics/twitter-message-service-pubsub'
        future = publisher.publish(topic_id, str.encode(message), school=school)
        future.result()