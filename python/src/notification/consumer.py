import pika,sys,os, time
from send import email
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    
    logger.info("Starting server consumer")    
    ## rabbitmq conn
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq")
    )
    
    def callback(ch, method, properties, body):
        err = email.notification(body)
        
        if err:
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)
    
    channel = connection.channel()
    channel.basic_consume(
        queue=os.environ.get('MP3_QUEUE'),
        on_message_callback=callback
    )
    
    logger.info("Waiting for messages. To exit press CTRL+C to quit.")
    
    channel.start_consuming()
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)