import re
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate
from ..validate.validation import validate_error as val
from django.utils.translation import gettext_lazy as _
from ..exception import CustomException

User = get_user_model()

class AlphaCharField(serializers.RegexField):
    def __init__(self, *args, **kwargs):
        kwargs['regex'] = r'^[a-zA-Z]+$'
        kwargs['error_messages'] = {'invalid': 'Please enter only alphabetic characters.'}
        super().__init__(*args, **kwargs)

class NumericField(serializers.RegexField):
    def __init__(self, *args, **kwargs):
        kwargs['regex'] = r'^\d+$'
        kwargs['error_messages'] = {'invalid': 'Please enter only numeric characters.'}
        super().__init__(*args, **kwargs)
        
class PhoneNumberField(serializers.RegexField):
    def __init__(self, *args, **kwargs):
        required = kwargs.pop('required', False)
        allow_blank = kwargs.pop('allow_blank', True)
        kwargs['regex'] = r'^\+1\(\d{3}\) \d{3}-\d{4}$'
        kwargs['error_messages'] = {'invalid': 'Please enter a valid US phone number in the format +1(XXX) XXX-XXXX.'}
        super().__init__(*args, **kwargs)
        self.required = required
        self.allow_blank = allow_blank
        
    def validate_empty_values(self, data):
        if data == '':
            self.fail('invalid')
        return super().validate_empty_values(data)

class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    first_name = AlphaCharField()
    last_name = AlphaCharField()
    street_address = serializers.CharField(max_length=255)
    city = serializers.CharField()
    postal_code = NumericField()
    country = serializers.CharField(max_length=255)
    phone_no = PhoneNumberField(required=True)
    state = serializers.CharField(max_length=255)
    class Meta:
        model = User
        fields = ('email', 'password',"phone_no",
                  'first_name', 'last_name'
        ,"street_address","city","postal_code","country","phone_no","state")
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if not email:
            message_info = val('EmailRequired')
            raise CustomException(detail=message_info['message'], status_code=message_info['code'])
        
        if not password:
            message_info = val('PasswordRequired')
            raise CustomException(detail=message_info['message'], status_code=message_info['code'])

        if User.objects.filter(email=email).exists() :
            message_info = val('EmailTaken')
            raise CustomException(detail=message_info['message'], status_code=message_info['code'])

        return data

    def validate_password(self, password):
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

        return password

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)


        user_email = User.objects.filter(email=email).first()
        user = authenticate(username=email, password=password)

        if not user and user_email:
            message_info = val('InvalidCredentials')            
            raise CustomException(detail=message_info['message'], status_code=message_info['code'])
        if not user:
            message_info = val('UserNotFound')            
            raise CustomException(detail=message_info['message'], status_code=message_info['code'])
        if not user.is_active:
            message_info = val('AccountNotActivated')
            raise CustomException(detail=message_info['message'], status_code=message_info['code'])
        return data
        

class AgentSignupSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        email = data.get('email')
        
        if User.objects.filter(email=email,is_active=True).exists() :
            message_info = val('EmailTaken')
            raise CustomException(detail=message_info['message'], status_code=message_info['code'])

        return data

class AgentSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = '__all__'
