import json

import pika
from utils import get_logger

logger = get_logger("Data Injector")


def send_to_rabbitmq(data: dict):
    connection = connect_rabbitmq()
    if connection is not None:
        channel = connection.channel()

        channel.queue_declare(queue="PremierLeague")
        logger.info(f"Sending data to RabbitMQ {data}")
        channel.basic_publish(
            exchange="",
            routing_key="PremierLeague",
            body=json.dumps(data),
        )
        logger.info(
            "Data sent to RabbitMQ and closing connection BlockingConnection with RabbitMQ.",
        )
        connection.close()
    else:
        logger.error(
            "Connection to RabbitMQ failed. Investigate the logs and connection to RabbitMQ service.",
        )


def connect_rabbitmq() -> pika.BlockingConnection | None:
    logger.info("Connecting to RabbitMQ...")
    connection = None
    # Trying to brute-forcely connect to RabbitMQ service with timeout 1min
    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host="rabbitmq",
                    port=5672,
                    socket_timeout=60,
                ),
            )
            logger.info("Connected to RabbitMQ")
            break
        # In case of ANY exceptions, trying to connect again
        except Exception:
            logger.info("Waiting for RabbitMQ")
            continue

    return connection


if __name__ == "__main__":
    print("Starting publisher")
