import json
import logging
import os
import sys

from kafka import KafkaProducer
from commands.create_user import CreateUser
from flask import request
from handlers.user_creation import UserCreationHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_message_kafka(bootstrap_servers: str, topic: str, message: dict):
    try:
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )

        producer.send(topic, message)
        producer.flush()
        logger.info(f"Message sent to topic '{topic}' successfully.")
    except Exception as e:
        logger.error(f"Failed to send message to Kafka: {e}")


def main():
    command = CreateUser(address="ktm", name="access")
    logger.info(f"System paths {sys.path}")

    message = UserCreationHandler.handle(command)
    i = 0
    while True:
        send_message_kafka(
            bootstrap_servers="my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092",  # Kafka service
            topic="request-topic",
            message={"name" : "Suman"},
        )
        i += 1
        if i == 100:
            break


    return {"msg": "Created Successfully"}

def consumer():
    body = request.get_json()
    logger.info(body)
    return {"status": 200, "body": body}
