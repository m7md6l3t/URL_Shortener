from app import create_app
from app.consumer import start_consumer


app = create_app()
start_consumer(app)  # Start the RabbitMQ consumer

if __name__ == '__main__':
    app.run(debug=True, port=5001)