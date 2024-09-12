import jwt
import datetime
from django.conf import settings
def token_generation(user_id):
    payload = {
        "user_id":user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token
    
            
           