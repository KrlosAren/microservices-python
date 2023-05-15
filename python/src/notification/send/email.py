import smtplib,os,json
from email.message import EmailMessage
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def notification(message):
    
    try:
        message = json.loads(message)
        mp3_fid = message['mp3_fid']
        sender_address = os.environ.get('GMAIL_SENDER_ADDRESS')
        sender_password = os.environ.get('GMAIL_SENDER_PASSWORD')
        receiver_address = message['username']
        
        msg =  EmailMessage()
        msg.set_content(f'Mp3 file_pid: http://mp3converter.com/download?fid={mp3_fid} is now ready to download!')
        msg['Subject'] = f'Mp3 Download'
        msg['From'] = sender_address
        msg['To'] = receiver_address
        
        session = smtplib.SMTP('smtp.gmail.com',587)
        session.starttls()
        session.login(sender_address,sender_password)
        session.send_message(msg,sender_address,receiver_address)
        session.quit()
        
        logger.info(f'Sending message')
        
    except Exception as err:
        logger.error(f'Error sending message to %s: %s' % (sender_address, err  % err))
        return err
    