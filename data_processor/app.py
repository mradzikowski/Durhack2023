import asyncio
import datetime
import json
import time

import pika
import pytz

from db.session import async_session
from models.fixtures import Fixture
from utils import get_logger

logger = get_logger("Data Processor")


async def process_message(data_retrieved):
    async with async_session() as session:
        for data in data_retrieved:
            if data["HomeTeam"] == "Spurs":
                logger.info("Spurs found, cleaning data to Tottenham")
                data["HomeTeam"] = "Tottenham"
            if data["AwayTeam"] == "Spurs":
                logger.info("Spurs found, cleaning data to Tottenham")
                data["AwayTeam"] = "Tottenham"

            try:
                if None in [data["HomeTeam"], data["AwayTeam"], data["HomeTeamScore"], data["AwayTeamScore"], data["DateUtc"]]:
                    logger.warning(f"KeyError: The date is not of expected error or the key is not present {data}")
                    continue
                session.add(
                    Fixture(
                        home_team=data["HomeTeam"],
                        away_team=data["AwayTeam"],
                        full_time_home_goals=int(data["HomeTeamScore"]),
                        full_time_away_goals=int(data["AwayTeamScore"]),
                        date=data["DateUtc"].split(" ")[0].replace("-", "/"),
                    ),
                )
            except KeyError as key_error:
                logger.warning(f"KeyError: The date is not of expected error or the key is not present {key_error}")
            except IndexError as index_error:
                logger.warning(f"IndexError: The date is not of expected format: {index_error}")
            else:
                logger.info(f"Added data for {data['HomeTeam']} vs {data['AwayTeam']} on {data['DateUtc'].split(' ')[0]}")
        await session.commit()


def callback(ch, method, properties, body):
    data_retrieved = json.loads(body)
    asyncio.run(
        process_message(data_retrieved),
    )  # Run the async function using asyncio.run


if __name__ == "__main__":
    print("Starting consumer")

    # Connect to RabbitMQ service with timeout 1min
    connection = None
    while not connection:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host="rabbitmq",
                    port=5672,
                    socket_timeout=60,
                ),
            )
            logger.info("Connected to RabbitMQ")
        except Exception as e:
            logger.warning(f"Waiting for RabbitMQ. Consumer cannot connect to RabbitMQ yet.")
            time.sleep(5)  # Sleep a bit before trying again

    while datetime.datetime.now(tz=pytz.timezone("Europe/London")).date() > datetime.datetime(2023, 11, 4).date():
        logger.info("Trying to scrape the data from the premier league"
                    " website to retrain the model and update the database.")
        time.sleep(1 * 60 * 60 * 24)

    channel = connection.channel()
    # Declare a queue
    channel.queue_declare(queue="PremierLeague")

    channel.basic_consume(
        queue="PremierLeague",
        auto_ack=True,
        on_message_callback=callback,
    )

    channel.start_consuming()
