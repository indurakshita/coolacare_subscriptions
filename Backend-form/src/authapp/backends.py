from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return

        user = User.objects.filter(email=username,is_active=True).first()
        if user is None:
            return
            
        if user.check_password(password):
            return user
