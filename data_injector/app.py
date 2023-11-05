import json
import os
import time
from collections import defaultdict
from datetime import datetime

import pika
from utils import get_logger

logger = get_logger("Data Injector")


def send_to_rabbitmq(data: list[dict]):
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
    with open("./dataset/2022-2023.json") as file:
        fixtures = json.load(file)

    games_by_date = defaultdict(list)
    for game in fixtures:
        date = datetime.strptime(game["DateUtc"], "%Y-%m-%d %H:%M:%S%z").date()

        games_by_date[date].append(game)

    sorted_dates = sorted(games_by_date.keys())

    for date in sorted_dates:
        # data_to_send = json.dumps()
        send_to_rabbitmq(games_by_date[date])
        logger.info(f"Sleeping for 60 seconds to imitating next day")
        time.sleep(60)
    logger("Starting producer")
