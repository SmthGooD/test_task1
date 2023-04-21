import jwt
from datetime import datetime, timedelta
from django.conf import settings


def generate_jwt_token(user_id):
    """
    Generates a JWT token for the given user ID.
    """
    token_expiry = datetime.utcnow() + timedelta(days=1)
    payload = {
        'user_id': user_id,
        'exp': token_expiry,
        'iat': datetime.utcnow(),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def verify_jwt_token(token):
    """
    Verifies the given JWT token and returns the user ID if the token is valid.
    Returns None if the token is invalid or has expired.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        return user_id
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        return None
