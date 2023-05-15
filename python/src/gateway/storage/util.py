import pika, json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def upload(file, fs, channel, access):
    
    try:
        fid = fs.put(file)
    except Exception as err:
        logger.info(f"Failed to upload file {err}")
        return "internal server error",500
    
    message =  {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"],
    }

    try:
        logger.info(f"Uploading file {str(fid)} => {message}")
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    
    except Exception as e:
        logger.info(f"Failed to publish video to channel  {e}")
        fs.delete(fid)
        return "internal server error", 500