from rest_framework import serializers
from django.contrib.auth.models import Group
from authapp.exception import CustomException
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class OTPGenerateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate(self, data):
        user = User.objects.filter(email=data['email']).first()
        if not user:
            raise CustomException(detail="User does not exist", status_code=status.HTTP_404_NOT_FOUND)
        
        required_groups = ['Admin', 'ProviderAdmin']
        if not any(group in required_groups for group in user.groups.values_list('name', flat=True)):
            raise CustomException(detail="User must be in the admin or provider admin group", status_code=status.HTTP_401_UNAUTHORIZED)
        
        return data




class OTPVerifySerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        
        try:
            admin_group = Group.objects.get(name='Admin')
        except Group.DoesNotExist:
            raise CustomException(detail="Admin group does not exist", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:  
            provider_admin_group = Group.objects.get(name='ProviderAdmin')
        except Group.DoesNotExist:
            raise CustomException(detail="Provider admin group does not exist", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if admin_group not in User.groups.all() and provider_admin_group not in User.groups.all():
            raise CustomException(detail="User must be in the admin or provider admin group", status_code=status.HTTP_401_UNAUTHORIZED)
        
        return data


