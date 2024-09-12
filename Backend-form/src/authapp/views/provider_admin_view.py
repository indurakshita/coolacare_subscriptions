from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authapp.serializers.reset_serializers import *
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from authapp.validate.validation import validate_response
from authapp.utils.email_send import Email_Sender
from authapp.exception import *
from authapp.permissions.group_permission import HasGroupPermission
from django.core.exceptions import ObjectDoesNotExist
from authapp.authentication import JWTAuthenticationBackend
from django.contrib.auth.models import Group
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

class AdminConvertionView(APIView):
    
    authentication_classes = [JWTAuthenticationBackend]
    model_name = 'customuser'
    permission_classes = [HasGroupPermission]
    serializer_class = AdminConvertionserializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            error = [f"{field} {error}" for field, errors in serializer.errors.items() for error in errors][0]
            raise CustomException(detail=error, status_code=status.HTTP_400_BAD_REQUEST)
        
        if not request.user.groups.filter(name="Admin").exists():
            raise CustomException(detail="You Don't Have Permission to Convert Agent to Admin", status_code=status.HTTP_403_FORBIDDEN)
        
        email = serializer.validated_data['email']
        user = User.objects.filter(email=email, groups__name='Agent').first()

        if not user:
            raise CustomException(detail="User Not Found or User Not Agent", status_code=status.HTTP_404_NOT_FOUND)

            
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = f"{settings.SITE_URL}/adminverify/?uid={uid}&token={token}"
        
        try:
            subject = 'Request for Admin Onboarding'
            Email_Sender(subject=subject,
                        template_name="AgentToAdmin.html",
                        context={"url":reset_url,"agent_email":user.email},
                        recipient_list=user.email
            )
        except Exception as e:
            raise CustomException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)
        
        user.save()
        
        return validate_response("AgentInviteToAdmin")



class AdminConvertionVerifyView(APIView):
    def get(self, request):
        uid = request.GET.get('uid')
        token = request.GET.get('token')
        
        if uid is None or token is None:
            raise CustomException(detail="Invalid Token", status_code=status.HTTP_400_BAD_REQUEST)
            
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)

            if user.is_provideradmin:
                raise CustomException(detail="User Already ProviderAdmin", status_code=status.HTTP_400_BAD_REQUEST)
            
            if default_token_generator.check_token(user, token):
                user.groups.add(Group.objects.get(name='ProviderAdmin'))
                user.is_provideradmin = True
                user.save()

                return validate_response("AgentInviteSuccess")

            else:
                raise CustomException(detail="Token Expired", status_code=status.HTTP_400_BAD_REQUEST)

        except ObjectDoesNotExist:
            raise CustomException(detail="User Not Found", status_code=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            raise CustomException(detail=str(e), status_code=status.HTTP_400_BAD_REQUEST)