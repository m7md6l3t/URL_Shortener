import pika
import json
from datetime import datetime
from .models import db, URL


# This function starts the RabbitMQ consumer
def start_consumer(app):
    # Establish a connection with RabbitMQ server.
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    # Create a new channel with the next available channel number or pass in a channel number to use.
    channel = connection.channel()
    # Declare a queue to communicate with RabbitMQ. If the queue doesn't exist, it will be created.
    channel.queue_declare(queue='URL_data', durable=True)

    # This function is called when a message is received
    def on_message_received(ch, method, properties, body):
        message = json.loads(body.decode())
        short_code = message.get("short_code")
        long_url = message.get("long_url")  # Assuming "original_url" is the correct key
        # Convert created_at to datetime object
        date_format = "%a, %d %b %Y %H:%M:%S %Z"
        created_at_datetime = datetime.strptime(message.get("created_at"), date_format)
        with app.app_context():
            new_url = URL(long_url=long_url, short_code=short_code, created_at=created_at_datetime)
            db.session.add(new_url)
            db.session.commit()

    # Set up a subscription on the queue
    channel.basic_consume(queue='URL_data', on_message_callback=on_message_received, auto_ack=True)
    print('Waiting for messages. To exit press CTRL+C')
    # Start consuming messages
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Interrupted by user, closing...")
        channel.stop_consuming()
        connection.close()