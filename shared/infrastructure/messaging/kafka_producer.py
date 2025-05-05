from kafka import KafkaProducer
from shared import Event
import json

class KafkaProducer:
    def __init__(self, bootstrap_servers: str, topic: str):
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
        self.topic = topic

    def start(self):
        self.producer.start()

    def stop(self):
        self.producer.stop()

    def publish(self, event: Event) -> None:
        event_data = {
            "event_id": event.event_id,
            "event_type": event.event_type,
            "timestamp": event.timestamp.isoformat(),
            **event.__dict__
        }
        self.producer.send_and_wait(
            self.topic, json.dumps(event_data).encode("utf-8")
        )