import logging

from flask import request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    # logger.info("This is consumer that is triggered")
    # logger.error("check if the consumer was triggered")
    body = request.get_json()
    logger.info(body)
    return {"status": 400, "body": "Consumer Response"}
