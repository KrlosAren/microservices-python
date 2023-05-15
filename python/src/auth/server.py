import os
from flask import Flask, request
from flask_mysqldb import MySQL

from utils.auth_jwt import  createJWT,decode_jwt

server = Flask(__name__)

mysql = MySQL(server)

## config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_PORT"] = 3307
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")

## api
@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "missing credentials", 401
    
    ## check db from username and password
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM users WHERE email = %s", (auth.username,)
    )
    
    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]
        cur.close()
        if auth.username != email or auth.password != password:
            return "invalid credentials", 401
        
        else:
            
            return createJWT(username=auth.username, secret=os.environ.get("JWT_SECRET"),auth=True)
    
    else:
        return "Invalid credentials", 401
    

@server.route('/validate', methods=['POST'])
def validate():
    
    encode_jwt = request.headers['Authorization']
    
    if not encode_jwt:
        return "missing credentials", 401
    
    return decode_jwt(encode_jwt=encode_jwt, secret=os.environ.get('JWT_SECRET')) 


if __name__ == "__main__":
    print(__name__)
    server.run(host='0.0.0.0', port=5000)