import json
import logging
import os
import sys

import pika
from commands.create_user import CreateUser
from flask import request
from handlers.user_creation import UserCreationHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_message_rabbitmq(host: str, queue: str, message: str):
    try:
        # Connect to RabbitMQ
        credentials = pika.PlainCredentials(
           "dummy-username", "dummy-password"
        )

        # Connect to RabbitMQ with authentication
        parameters = pika.ConnectionParameters(host=host, credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        # Declare the queue (idempotent)
        channel.queue_declare(queue=queue, durable=True)

        # Publish message
        channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2),  # make message persistent
        )

        logger.info(f"Message sent to queue '{queue}' successfully.")

    except Exception as e:
        logger.error(f"Failed to send message to RabbitMQ: {e}")
    finally:
        if "connection" in locals() and connection.is_open:
            connection.close()


def main():
    command = CreateUser(address="ktm", name="access")
    logger.info(f"System paths {sys.path}")

    message = UserCreationHandler.handle(command)

    send_message_rabbitmq(
        host="rabbitmq-events.default.svc.cluster.local",  # RabbitMQ service hostname
        queue="request-topic",  # Equivalent to Kafka's topic
        message=message,
    )

    return {"msg": "Created Successfully"}


def consumer():
    logger.info("This is consumer that is triggered")
    logger.error("check if the consumer was triggered")
    body = request.get_json()
    logger.info(body)
    return {"status": 400, "body": "Consumer Response"}
