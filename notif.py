from concurrent import futures
from google.cloud import pubsub_v1
from typing import Callable

# projects/review-management-402504/topics/deleted-review
project_id = "review-management-402504"
topic_id = "deleted-review"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)
publish_futures = []

def get_callback(
    publish_future: pubsub_v1.publisher.futures.Future, data: str
) -> Callable[[pubsub_v1.publisher.futures.Future], None]:
    def callback(publish_future: pubsub_v1.publisher.futures.Future) -> None:
        try:
            # Wait 60 seconds for the publish call to succeed.
            print(publish_future.result(timeout=60))
        except futures.TimeoutError:
            print(f"Publishing {data} timed out.")

    return callback

def send_deleted_notif():
    msg = "Review has been deleted"
    publish_future = publisher.publish(topic_path, msg.encode("utf-8"))
    publish_future.add_done_callback(get_callback(publish_future, msg))
    publish_futures.append(publish_future)

    futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

    print(f"Published message to {topic_path}.")

