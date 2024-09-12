from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authapp.serializers.auth_serializer import (
    SignupSerializer, LoginSerializer,AgentSignupSerializer
)
from authapp.serializers.reset_serializers import *
from authapp.serializers.userprofile import UserSerializer
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from authapp.validate.validation import validate_response
from authapp.utils.email_send import Email_Sender
from authapp.utils.token import token_generation
from authapp.exception import *
from django.core.exceptions import ObjectDoesNotExist
from authapp.authentication import JWTAuthenticationBackend
from subscription.models.avaialbleslots import AvailableSlots


User = get_user_model()
default_from_email = settings.EMAIL_HOST_USER

class SignupView(APIView):
    serializer_class = SignupSerializer

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            user = serializer.save()
            user.groups.add(3)  # Assuming group 3 is for customer users
            email = serializer.validated_data.get("email")
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            url = f"{settings.SITE_URL}/activateAccount?uid={uid}&token={token}"
            subject = 'Activate Your Account'
            Email_Sender(subject=subject,
                            template_name="SignupActivationMail.html",
                            context={
                                "url":url,
                                "username":user.email
                            },
                        recipient_list=email
                        )
            return validate_response("Customercreated")
        else:
            error = [f"{field} {error}" for field, errors in serializer.errors.items() for error in errors][0]
            raise CustomException(detail=error, status_code=status.HTTP_400_BAD_REQUEST)
    


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user and user.is_active:
                if user.groups.filter(name__in=["Admin","ProviderAdmin"] ).exists():
                    api_url = f'{settings.SITE_URL}/api/auth/generate-otp/'
                    return Response({
                    "message": "Generate OTP Using Below URL",
                    "email": user.email,
                    "group" : "ProviderAdmin" if user.groups.filter(name="ProviderAdmin").exists() else "Admin",
                    "url": api_url
                    }, status=status.HTTP_200_OK)

                else:
                    token = token_generation(user_id=user.id)
                    login(request, user)
                    return Response({
                    "message": {
                    "user": user.id,
                    "group": user.groups.all()[0].name if user.groups.exists() else None, 
                    "token" : token
                    }
                    }, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid credentials or account not active"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            error = [f"{field} {error}" for field, errors in serializer.errors.items() for error in errors][0]
            raise CustomException(detail=error, status_code=status.HTTP_400_BAD_REQUEST)


class AgentSignupView(APIView):
    serializer_class = AgentSignupSerializer
    
    def post(self, request):
        serializer = AgentSignupSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            try:
                user = User.objects.get(email=email,is_active=False)
                user.status = True
                user.save()
                self.send_password_set_email(user)
                return validate_response("Agentcreated")
            except ObjectDoesNotExist:
                user = User.objects.create_user(email=email)
                user.groups.add(2)
                user.status = True
                self.send_password_set_email(user)
                return validate_response("Agentcreated")
        else:
            error = [f"{field} {error}" for field, errors in serializer.errors.items() for error in errors][0]
            raise CustomException(detail=error, status_code=status.HTTP_400_BAD_REQUEST)
        

    def send_password_set_email(self, user):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        password_reset_url = f"{settings.SITE_URL}/userAgent?uid={uid}&token={token}"
        subject = 'Set Up Your Password'
        Email_Sender(subject=subject,
                    template_name="OnboardingCreatePassword.html",
                    context={"url":password_reset_url,"username":user.email},
                    recipient_list=user.email
            )


class UserProfileApi_view(APIView):
    def get(self, request, pk=None):
        try:
            user_profile = User.objects.get(id=pk)
            serializer = UserSerializer(user_profile)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        user_id = request.data.get("id")
        try:
            user_profile = User.objects.get(id=user_id)
            serializer = UserSerializer(user_profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"Profile Updated Successfully"},status=200)
            error = [f"{field} {error}" for field, errors in serializer.errors.items() for error in errors][0]
            raise CustomException(detail=error, status_code=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)



class AgentView(APIView):
    authentication_classes = [JWTAuthenticationBackend]

    def delete(self, request):
        if not request.user.groups.filter(name="Admin").exists():
            raise CustomException(detail="You Don't Have Permission Creat Subscription", status_code=status.HTTP_403_FORBIDDEN)

        email = request.query_params.get('email')
        if not email:
            return validate_response("InvalidAgentId")

        try:
            instance = User.objects.get(email=email, groups__name='Agent')
            # Reduce available slots by 1
            if instance.is_active:
                available_slot = AvailableSlots.objects.all()
                for slot in available_slot:
                    slot.total_slots -= 4
                    slot.available_slots -= 4
                    slot.save()
            instance.is_active = False
            instance.status = False
            instance.save()
            return validate_response("AgentDeleted")

        except ObjectDoesNotExist:
            return validate_response("AgentNotFound")
        


        





                

