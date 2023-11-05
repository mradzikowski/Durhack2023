# import json
#
# import pika
#
# from db.session import async_session
# from models.fixtures import Fixture
# from utils import get_logger
#
# logger = get_logger("Data Processor")
#
#
# if __name__ == "__main__":
#     print("Starting consumer")
#
#     async def callback(ch, method, properties, body):
#         data_retrieved: list[dict] = json.loads(body)
#         with async_session() as session:
#             for data in data_retrieved:
#                 session.add(
#                     Fixture(
#                         home_team=data["HomeTeam"],
#                         away_team=data["AwayTeam"],
#                         full_time_home_goals=int(data["HomeTeamScore"]),
#                         full_time_away_goals=int(data["AwayTeamScore"]),
#                         date=data["DateUtc"].split(" ")[0].replace("-", "/"),
#                     )
#             )
#             await session.commit()
#
#
#         print(f"Received message {json.loads(body)}")
#
#     # Connect to RabbitMQ service with timeout 1min
#     while True:
#         try:
#             connection = pika.BlockingConnection(
#                 pika.ConnectionParameters(
#                     host="rabbitmq",
#                     port=5672,
#                     socket_timeout=60,
#                 ),
#             )
#             print("Connected to RabbitMQ")
#             break
#         except Exception:
#             print("Waiting for RabbitMQ")
#             continue
#
#     channel = connection.channel()
#     # Declare a queue
#     channel.queue_declare(queue="PremierLeague")
#
#     channel.basic_consume(
#         queue="PremierLeague",
#         auto_ack=True,
#         on_message_callback=callback,
#     )
#
#     channel.start_consuming()


import asyncio
import json
import time

import pika

from db.session import async_session
from models.fixtures import Fixture
from utils import get_logger

logger = get_logger("Data Processor")


async def process_message(data_retrieved):
    async with async_session() as session:
        for data in data_retrieved:
            if data["HomeTeam"] == "Spurs":
                data["HomeTeam"] = "Tottenham"
            if data["AwayTeam"] == "Spurs":
                data["AwayTeam"] = "Tottenham"

            session.add(
                Fixture(
                    home_team=data["HomeTeam"],
                    away_team=data["AwayTeam"],
                    full_time_home_goals=int(data["HomeTeamScore"]),
                    full_time_away_goals=int(data["AwayTeamScore"]),
                    date=data["DateUtc"].split(" ")[0].replace("-", "/"),
                )
        )
        await session.commit()

def callback(ch, method, properties, body):
    data_retrieved = json.loads(body)
    asyncio.run(process_message(data_retrieved))  # Run the async function using asyncio.run
    print(f"Received message {data_retrieved}")

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
                )
            )
            print("Connected to RabbitMQ")
        except Exception as e:
            print(f"Waiting for RabbitMQ: {e}")
            time.sleep(5)  # Sleep a bit before trying again

    channel = connection.channel()
    # Declare a queue
    channel.queue_declare(queue="PremierLeague")

    channel.basic_consume(
        queue="PremierLeague",
        auto_ack=True,
        on_message_callback=callback,
    )

    channel.start_consuming()
