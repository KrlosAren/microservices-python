import  jwt, datetime

def createJWT(username, secret, auth):
    
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin":auth
        },
        secret,
        algorithm='HS256'
    )
    
def decode_jwt(encode_jwt, secret):
    encode_jwt = encode_jwt.split(' ')[1]
    
    try:
        decoded = jwt.decode(encode_jwt, secret,algorithms=['HS256'])
    except Exception as error:
        print(f'Error decoding jwt: %s' % error)
        return ("not authorized", 403)
    
    return (decoded, 200)