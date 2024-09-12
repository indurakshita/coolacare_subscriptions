import pyotp
from rest_framework import status
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from authapp.exception import CustomException
from authapp.serializers.otp_serializers import OTPGenerateSerializer ,OTPVerifySerializer
from authapp.utils.email_send import Email_Sender
from django.contrib.auth import get_user_model
from authapp.utils.token import token_generation
from django.contrib.auth import login
from django.conf import settings
from authapp.models.otpmodel import OTP
import base64


User = get_user_model()


class OTPGenerateView(APIView):
    serializer_class = OTPGenerateSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            error = [f"{field} {error}" for field, errors in serializer.errors.items() for error in errors][0]
            raise CustomException(detail=error, status_code=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email=request.data["email"]).first()
        secret_key = base64.b32encode(user.email.encode()) 
        totp = pyotp.TOTP(secret_key, interval=1)
        otp = totp.now()
        existing_otp = OTP.objects.filter(user=user).first()

        if existing_otp:
            existing_otp.delete()

        OTP(user=user,otp=otp).save()

        Email_Sender(subject='Your OTP', template_name="OtpTemplate.html", context={"otp":otp}, recipient_list=serializer.data["email"])

        return Response({"Type":"Success",
                        'message': 'OTP sent to email Please verify otp using below link',
                         "url": f'{settings.SITE_URL}/api/auth/verify-otp/'}, 
                         status=status.HTTP_200_OK)





class OTPVerifyView(APIView):
    serializer_class = OTPVerifySerializer
    
    def post(self, request):
        otp_value = request.data.get('otp')
        try:
            otp = OTP.objects.get(otp=otp_value)
        except OTP.DoesNotExist:
            raise CustomException(detail="Invalid OTP", status_code=status.HTTP_400_BAD_REQUEST)
        
        if timezone.now() > otp.created_at + timezone.timedelta(minutes=5):
            raise CustomException(detail="OTP Expired", status_code=status.HTTP_400_BAD_REQUEST)
    
        if otp_value == otp.otp:
            user = User.objects.get(id=otp.user_id)
            token = token_generation(user_id=user.id)
            login(request, user)
            return Response({
                "type": "Success",
                "message": {
                    "user": user.id,
                    "group" : "ProviderAdmin" if user.groups.filter(name="ProviderAdmin").exists() else "Admin",
                    "token" : token
                }
            }, status=status.HTTP_200_OK)
        else:
            raise CustomException(detail="Invalid OTP", status_code=status.HTTP_400_BAD_REQUEST)










