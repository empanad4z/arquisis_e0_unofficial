import os
import ssl
import pika
import time
from dotenv import load_dotenv

def callback(ch, method, properties, body):
    print(f" [x] {body}")

load_dotenv()

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_options = pika.SSLOptions(ssl_context, 'broker.iic2173.org')

url = os.getenv('AMQP_URL')
params = pika.URLParameters(url)
connection = None

while True:
    try:
        print(' Connecting...')
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.exchange_declare(exchange='energy.x', passive=True)
        result = channel.queue_declare(queue='observer.37.q', durable=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange='energy.x', queue=queue_name)

        print(' [*] Waiting for logs. To exit press CTRL+C')
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()

    except KeyboardInterrupt as e:
        print('\n [!] Detenido por el usuario.')
        if connection and connection.is_open:
            connection.close()
        break
    except Exception as e:
        print(f' [!] Error: {e!r}')
        print(' [!] Intentando reconectar en 5 segundos...')
        time.sleep(5)
        import time
