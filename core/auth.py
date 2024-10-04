from jose import jwt
from django.conf import settings
from datetime import datetime, timedelta
from core.models import CustomUser as User
from django.utils import timezone
from ninja.security import HttpBearer

from core.signals import logger

def create_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.now() + timedelta(days=1),
        'iat': datetime.now(),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def get_user_from_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user = User.objects.get(id=payload['user_id'])
        return user
    except jwt.ExpiredSignatureError:
        logger.warning("Token has expired")
    except jwt.JWTError as e:
        logger.error(f"JWT Error: {str(e)}")
    except User.DoesNotExist:
        logger.warning("User not found")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
    return None


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        logger.debug(f"Authenticating token: {token[:10]}...")
        print(f"AuthBearer.authenticate called with token: {token}")

        try:
            user = get_user_from_token(token)
            if user:
                print(f"Authenticated user: {user.username}")
                logger.debug(f"Authenticated user: {user.username}")
                request.auth = user
                return user
            else:
                logger.warning("User not found for token")
        except Exception as e:
            logger.error(f"Error decoding JWT token: {str(e)}")
        logger.warning("Authentication failed")
        return None

auth = AuthBearer()