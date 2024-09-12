from rest_framework.views import APIView
from rest_framework import status
from authapp.serializers.reset_serializers import (
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer,
    AgentSetPasswordSerializer
    
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from authapp.validate.validation import validate_response
from authapp.utils.email_send import Email_Sender
from django.contrib.auth.hashers import check_password
from authapp.exception import *
from subscription.models.avaialbleslots import AvailableSlots


User = get_user_model()
default_from_email = settings.EMAIL_HOST_USER

class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_url = f"{settings.SITE_URL}/resetPassword?uid={uid}&token={token}"
                subject = 'Password Reset Request'
                Email_Sender(subject=subject,
                            template_name="ChangePassword.html",
                            context={"url":reset_url,"username":user.email},recipient_list=user.email
                    )
                return validate_response("PasswordResetEmailSent")
            else:
                return validate_response("UserNotFound")
        else:
            error = [f"{field} {error}" for field, errors in serializer.errors.items() for error in errors][0]
            raise CustomException(detail=error, status_code=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    def post(self, request):
        uid = request.GET.get('uid')
        token = request.GET.get('token')
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            if uid is None or token is None:
                return validate_response("InvalidToken")
            try:
                uid = force_str(urlsafe_base64_decode(uid))
                user = User.objects.get(pk=uid)
                if default_token_generator.check_token(user, token):
                    password = serializer.validated_data.get("new_password")
                    if check_password(password,user.password):
                        return validate_response("PasswordReuseError")
                    user.set_password(password)
                    user.save()
                    return validate_response("PasswordResetSuccess")
                else:
                    return validate_response("PasswordResetLinkExpired")
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return validate_response("PasswordResetLinkExpired")
        else:
            error = [f"{field} {error}" for field, errors in serializer.errors.items() for error in errors][0]
            raise CustomException(detail=error, status_code=status.HTTP_400_BAD_REQUEST)
    

class AgentSetPasswordView(APIView):
    serializer_class = AgentSetPasswordSerializer
    
    def post(self, request):
        uid = request.GET.get('uid')
        token = request.GET.get('token')
        serializer = AgentSetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            if uid is None or token is None:
                return validate_response("InvalidToken")
            try:
                is_active = serializer.validated_data.get('is_active')
                uid = force_str(urlsafe_base64_decode(uid))
                user = User.objects.get(pk=uid)
                
                if default_token_generator.check_token(user, token):
                    password = serializer.validated_data.get("password")
                    user.set_password(password)
                    user.is_active=is_active
                    user.save()
                    slotes = AvailableSlots.objects.all()
                    for sl in slotes:
                        sl.total_slots += 4
                        sl.available_slots += 4
                        sl.save()
                    subject = 'Password Set Successfully'
                    Email_Sender(subject=subject,
                                template_name="OnboardingAgentSuccessMessage.html",
                                context={"username":user.email},recipient_list=user.email
                        )
            
                    return validate_response("PasswordSetSuccess")
                else:
                    return validate_response("PasswordResetLinkExpired")
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return validate_response("PasswordResetLinkExpired")
        else:
            error = [f"{field} {error}" for field, errors in serializer.errors.items() for error in errors][0]
            raise CustomException(detail=error, status_code=status.HTTP_400_BAD_REQUEST)