import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from authapp.exception import CustomException
User = get_user_model()

class JWTAuthenticationBackend(BaseAuthentication):
    def authenticate(self, request, token=None):
        if token is None:
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            if not auth_header:
                raise CustomException(detail='Authentication failed. Provide a valid token in the header.',status_code=400)
            token = auth_header

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            print(payload)
            user_id = payload.get('user_id')
            user = User.objects.get(pk=user_id)
            return (user, None)
        except jwt.ExpiredSignatureError:
            raise CustomException(detail='Token has expired',status_code=400)
        except jwt.InvalidTokenError:
            raise CustomException(detail='Invalid token',status_code=400)
        except User.DoesNotExist:
            raise CustomException(detail='User not found',status_code=400)
        