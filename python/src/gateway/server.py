import os, gridfs, pika, json
from flask import Flask, request,send_file
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

import logging

from auth import access
from auth_svc import validate

from storage import util

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

## server
server = Flask(__name__)

mongo_video = PyMongo(
    server,
    uri=f"mongodb://host.minikube.internal:28017/videos"
)

mongo_mp3 = PyMongo(
    server,
    uri=f"mongodb://host.minikube.internal:28017/mp3s"
)

## chunks size of files in mongodb when content is more than 16mb
fs_videos= gridfs.GridFS(mongo_video.db)
fs_mp3s = gridfs.GridFS(mongo_mp3.db)

## rabbitmq conn 
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()


@server.route('/login',methods=['POST'])
def login():
    
    token ,err = access.login(request)
    
    if not err:
        return token
    else:
        return err
    
    
@server.route('/upload', methods=['POST'])
def upload():
    
    access , err = validate.token(request)
    
    if err:
        return err
    
    access = json.loads(access)
    
    if access["admin"]:
        if len(request.files) > 1 or len(request.files) < 1:
            return "exactly 1 file required", 400        
        for _,file in request.files.items():
            err = util.upload(file, fs_videos, channel, access)
            if err:
                return err
        return "success!", 200
    else:
        return "not authorized",401
    

@server.route("/download", methods=["GET"])
def download():
    
    access , err = validate.token(request)
    
    if err:
        return err
    
    access = json.loads(access)
    if access["admin"]:
        
        fid_string = request.args.get("fid")
        
        if not fid_string :
            return "fid is required"
        
        try:
            out = fs_mp3s.get(ObjectId(fid_string))
            return send_file(out, download_name=f"{fid_string}.mp3")
        
        except Exception as err:
            logger.error(f"Failed to retrieve {err}")
            return "internal error", 500
    
    return "not authorized", 401        
        

    
    


if __name__ == "__main__":
    server.run(host='0.0.0.0', port=8080)