from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from ..exception import CustomException
from ..validate.validation import validate_error as val
import re

User = get_user_model()

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not value:
            message_info = val('EmailRequired')
            raise CustomException(detail=message_info['message'], status_code=message_info['code'])
        
        if value:
            if not User.objects.filter(email=value):
                message_info = val('UserNotFound')            
                raise CustomException(detail=message_info['message'], status_code=message_info['code'])

            if not User.objects.filter(email=value, is_active=True).exists():
                message_info = val('AccountNotActivated')
                raise CustomException(detail=message_info['message'], status_code=message_info['code'])

        return value
            

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField()

    def validate(self, data):
        password = data.get('new_password', None)
        if password is None:
            message_info = val('PasswordRequired')            
            raise CustomException(detail=message_info['message'], status_code=message_info['code'])
        
        if len(password) < 8:
            message_info = val('PasswordTooShort')
            raise CustomException(detail=message_info['message'], status_code=message_info['code'])

        if not re.search(r'[A-Z]', password):
            message_info = val('PasswordNoUppercase')
            raise CustomException(detail=message_info['message'], status_code=message_info['code'])

        if not re.search(r'[a-z]', password):
            message_info = val('PasswordNoLowercase')
            raise CustomException(detail=message_info['message'], status_code=message_info['code'])

        if not re.search(r'\d', password):
            message_info = val('PasswordNoDigit')
            raise CustomException(detail=message_info['message'], status_code=message_info['code'])

        if not re.search(r'[!@#$%^&*()_+=\-[\]{};:\'",.<>/?]', password):
            message_info = val('PasswordNoSpecialCharacter')
            raise CustomException(detail=message_info['message'], status_code=message_info['code'])

        common_passwords = ['password', '123456', 'qwerty', 'letmein', 'admin']
        if password.lower() in common_passwords:
            message_info = val('PasswordTooCommon')
            raise CustomException(detail=message_info['message'], status_code=message_info['code'])

        return data


class AgentSetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    is_active = serializers.BooleanField()

    def validate(self, data):
        password = data.get('password', None)
        is_active = data.get('is_active')
        if password is None:
            message_info = val('PasswordRequired')            
            raise CustomException(detail=message_info['message'], status_code=message_info['code'])
        
        if not is_active :
            raise CustomException(detail="is active must be True", status_code=400)
        
        if len(password) < 8:
            message_info = val('PasswordTooShort')
            raise CustomException(detail=message_info['message'], status_code=message_info['code'])

        if not re.search(r'[A-Z]', password):
            message_info = val('PasswordNoUppercase')
            raise CustomException(detail=message_info['message'], status_code=message_info['code'])

        if not re.search(r'[a-z]', password):
            message_info = val('PasswordNoLowercase')
            raise CustomException(detail=message_info['message'], status_code=message_info['code'])

        if not re.search(r'\d', password):
            message_info = val('PasswordNoDigit')
            raise CustomException(detail=message_info['message'], status_code=message_info['code'])

        if not re.search(r'[!@#$%^&*()_+=\-[\]{};:\'",.<>/?]', password):
            message_info = val('PasswordNoSpecialCharacter')
            raise CustomException(detail=message_info['message'], status_code=message_info['code'])

        common_passwords = ['password', '123456', 'qwerty', 'letmein', 'admin']
        if password.lower() in common_passwords:
            message_info = val('PasswordTooCommon')
            raise CustomException(detail=message_info['message'], status_code=message_info['code'])

        return data
    

class AdminConvertionserializer(serializers.Serializer):
    email = serializers.EmailField()
    