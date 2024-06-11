from flask import json
import pika


def connect_to_rabbitmq():
    """Establishes a connection to the RabbitMQ server."""
    credentials = pika.PlainCredentials("guest", "guest")  # Replace with your credentials
    parameters = pika.ConnectionParameters(host="localhost", credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    return connection.channel()

def publish_message(channel, exchange, routing_key, message):
    """Publishes a message to RabbitMQ."""
    channel.basic_publish(exchange=exchange, routing_key=routing_key, body=json.dumps(message))