import json
import logging
import sys

from kafka import KafkaProducer
from access_management.application.commands.create_user import CreateUser
from flask import request

from access_management.application.services.user_service import create_user
from access_management.domain.aggregates.user import User
from access_management.domain.value_objects.email import Email
from access_management.handlers.user_creation import UserCreationHandler

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

    user = create_user(User(username="suman", password="User1234@", email=Email(value="suman.gole@truenary.com")))
    send_message_kafka(topic="request-topic", message="user.created", bootstrap_servers="my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092")
    return {"msg" : user.__dict__}

def consumer():
    body = request.get_json()
    method = request.method
    route = request.root_url

    logger.info(f"{body} {method} {route}")
    return {"status": 200, "body": body}
