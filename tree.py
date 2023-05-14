import jwt
from datetime import datetime, timedelta

def expiry_date():
	return datetime.utcnow() + timedelta(seconds=Config.JWT_EXPIRY)

def generate_jwt(payload, expiry=expiry_date(), secret=None):
    _payload = {
        'iss': "chat-service",
        'exp': expiry,
        }
    _payload.update(payload)
        
    if not secret:
        secret = Config.JWT_SECRET
        
    token = jwt.encode(_payload, secret, algorithm='HS256')
    return token


def verify_jwt(token, secret=None):
    if not secret:
        secret = Config.JWT_SECRET
        
    try:
        payload = jwt.decode(token, secret, algorithms='HS256')
        print(payload)
    except jwt.PyJWTError:
        payload = None
    
    return payload


token = 'eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyaWQiOjkxMzgzMDAsImJsb2NrZWQiOmZhbHNlfQ.BIv76e7HTtvmW8gE0NEzKDYn5ByRvzcpip-hzoMAdjA'
secret = ''
verify_jwt(token, '')