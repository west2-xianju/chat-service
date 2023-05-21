import jwt
from app import Config
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
        secret = Config.JWT_SECRET or ''

    token = jwt.encode(_payload, secret, algorithm='HS256')
    return token


def verify_jwt(token, secret=None):
    if not secret:
        secret = Config.JWT_SECRET

    try:
        payload = jwt.decode(token, secret, algorithms='HS256')
        # print(payload)
    except:
        payload = None

    return payload
