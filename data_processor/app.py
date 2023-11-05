import json

import pika
from utils import get_logger

logger = get_logger("Data Processor")


if __name__ == "__main__":
    print("Starting consumer")

    def callback(ch, method, properties, body):
        pass

    # Connect to RabbitMQ service with timeout 1min
    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host="rabbitmq",
                    port=5672,
                    socket_timeout=60,
                ),
            )
            print("Connected to RabbitMQ")
            break
        except Exception:
            print("Waiting for RabbitMQ")
            continue

    channel = connection.channel()
    # Declare a queue
    channel.queue_declare(queue="PremierLeague")

    channel.basic_consume(
        queue="PremierLeague",
        auto_ack=True,
        on_message_callback=callback,
    )

    channel.start_consuming()
