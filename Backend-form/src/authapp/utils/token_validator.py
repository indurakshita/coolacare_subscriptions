import jwt
from django.contrib.auth import get_user_model
User = get_user_model()

def validate_access_token(token):
    try:
        secret_key = "https://subscription.coolocare.com/access/validation"
        decoded_payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return True

    except Exception:
        return False
    

def user_getter(token):
    try:
        secret_key = "https://subscription.coolocare.com/access/validation"
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        user_id = payload.get('user_id')
        user = User.objects.get(pk=user_id)
        return user

    except Exception:
        return "not work"