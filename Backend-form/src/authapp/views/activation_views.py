from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from authapp.validate.validation import validate_response
User = get_user_model()

class ActivateUserView(APIView):
    def get(self, request):
        try:
            uidb64 = request.GET.get('uid')
            token = request.GET.get('token')
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user is not None and default_token_generator.check_token(user, token):
            if user.is_active==True:
                return validate_response("UserAlreadyActivated")
            user.is_active = True
            user.save()
            return validate_response("AccountActivated")
        else:
            return validate_response("InvalidActivationLink")
