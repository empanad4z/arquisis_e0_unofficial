import logging
import os
import ssl
import pika
import time
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def callback(ch, method, properties, body):
    logger.info("Received message: %s", body)

load_dotenv()

ssl_context = ssl.create_default_context()
ssl_options = pika.SSLOptions(ssl_context, 'broker.iic2173.org')

url = os.getenv('AMQP_URL')
params = pika.URLParameters(url)
params.ssl_options = ssl_options
connection = None

while True:
    try:
        logger.info("Connecting...")
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        result = channel.queue_declare(queue='observer.37.q', passive=True)
        queue_name = result.method.queue

        logger.info("Waiting for messages. To exit press CTRL+C")
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()

    except KeyboardInterrupt:
        logger.info("Detenido por el usuario.")
        if connection and connection.is_open:
            connection.close()
        break
    except Exception:
        logger.exception("Error de conexion. Intentando reconectar en 5 segundos...")
        time.sleep(5)
