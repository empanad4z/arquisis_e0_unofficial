import json
import logging
import os
import ssl
import time
from pathlib import Path

import pika
import requests
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

load_dotenv()

MASTER_API_URL = os.getenv("MASTER_API_URL", "http://master:8000").rstrip("/")
EVENTS_ENDPOINT = f"{MASTER_API_URL}/events"
REQUEST_TIMEOUT = float(os.getenv("MASTER_API_TIMEOUT", "5"))
RETRY_DELAY = float(os.getenv("MASTER_API_RETRY_DELAY", "5"))
HEALTH_FILE = Path(os.getenv("HEALTH_FILE", "/tmp/healthy"))

http = requests.Session()


def callback(ch, method, properties, body):
    HEALTH_FILE.touch()
    logger.info("Received message: %s", body)

    try:
        event = json.loads(body)
    except json.JSONDecodeError:
        logger.exception("El mensaje no es JSON valido, se descarta")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    try:
        response = http.post(EVENTS_ENDPOINT, json=event, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.HTTPError as exc:
        status = exc.response.status_code
        if 400 <= status < 500:
            logger.error("Master rechazo el evento (%s): %s", status, exc.response.text)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            logger.error("Error del master (%s), se reencola el evento", status)
            time.sleep(RETRY_DELAY)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        return
    except requests.RequestException:
        logger.exception("No se pudo contactar al master, se reencola el evento")
        time.sleep(RETRY_DELAY)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        return

    result = response.json()
    logger.info("Evento guardado en master: id=%s", result.get("id"))
    ch.basic_ack(delivery_tag=method.delivery_tag)


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

        channel.basic_qos(prefetch_count=1)

        logger.info("Waiting for messages. To exit press CTRL+C")
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)
        channel.start_consuming()

    except KeyboardInterrupt:
        logger.info("Detenido por el usuario.")
        if connection and connection.is_open:
            connection.close()
        break
    except Exception:
        logger.exception("Error de conexion. Intentando reconectar en 5 segundos...")
        time.sleep(5)
