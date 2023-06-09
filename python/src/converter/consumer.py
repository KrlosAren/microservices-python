import pika,sys,os, time
from pymongo import MongoClient
import gridfs
from convert import to_mp3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    
    logger.info("Starting server consumer")
    
    client = MongoClient("host.minikube.internal",28017)
    db_videos = client.videos
    db_mp3s = client.mp3s
    
    ## gridfs
    fs_videos = gridfs.GridFS(db_videos)
    fs_mp3s = gridfs.GridFS(db_mp3s)
    
    ## rabbitmq conn
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq")
    )
    
    def callback(ch, method, properties, body):
        logger.info("Callback called with body: %s", body)
        err = to_mp3.start(body, fs_videos, fs_mp3s, ch)
        
        logger.info("Error: %s", err)
        
        if err:
            logger.info("Error: %s", err )
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            logger.info("Successfully started callback with body: %s", body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
    
    channel = connection.channel()
    logger.info("Connecting to %s", channel)
    channel.basic_consume(queue=os.environ.get('VIDEO_QUEUE'),on_message_callback=callback)
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