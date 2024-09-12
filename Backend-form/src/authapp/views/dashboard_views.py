from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from authapp.validate.validation import validate_response
from authapp.serializers.dash_board_serializer import AgentSerializer,CustomerSerializer
from authapp.permissions.group_permission import HasGroupPermission
from authapp.authentication import JWTAuthenticationBackend
from authapp.filters.AgentFilter import AgentFilter
from authapp.filters.CustomerFilter import CustomerFilter
from django.contrib.auth.models import Group
from authapp.exception import *
User = get_user_model()


class AgentListView(APIView):
    authentication_classes = [JWTAuthenticationBackend]
    model_name = 'customuser'
    permission_classes = [HasGroupPermission]
    serializer_class = AgentSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name__in=['Admin','ProviderAdmin']).exists():

            queryset = User.objects.filter(groups__name="Agent",status=True)
            user_filter = AgentFilter(self.request.GET, queryset=queryset)
            queryset = user_filter.qs
            return queryset
        else:
            return User.objects.none()

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
        

    def delete(self, request):
        id = request.data.get('id') 
        if id:
            try:
                user = User.objects.get(pk=id) 
            except User.DoesNotExist:
                raise CustomException(detail="User does not exist", status_code=status.HTTP_404_NOT_FOUND)

            if user.groups.filter(name='ProviderAdmin').exists():
                try:
                    user.groups.remove(Group.objects.get(name='ProviderAdmin'))
                    user.is_provideradmin = False
                    user.save()
                except Group.DoesNotExist:
                    raise CustomException(detail="Agent group does not exist", status_code=status.HTTP_404_NOT_FOUND)

                user.save()
                return validate_response("AdminAccessRevoke")

            else:
                raise CustomException(detail="User is not an ProviderAdmin", status_code=status.HTTP_400_BAD_REQUEST)
        else:
            raise CustomException(detail="Invalid user id", status_code=status.HTTP_400_BAD_REQUEST)

    


class CustomerListView(APIView):
    authentication_classes = [JWTAuthenticationBackend]
    model_name = "customuser".lower()
    permission_classes = [HasGroupPermission]
    serializer_class = CustomerSerializer

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name__in=['Admin','ProviderAdmin']).exists():
            queryset = User.objects.filter(groups__name="Customer",status=True)
            user_filter = CustomerFilter(self.request.GET, queryset=queryset)
            queryset = user_filter.qs
            return queryset
        else:
            return User.objects.none()

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
    def delete(self, request):
        id = request.data.get('id')
        if id:
            try:
                user = User.objects.get(pk=id)
                if user.groups.filter(name='Customer').exists():
                    user.delete()
                    return validate_response("CustomerDelete")
                else:
                    raise CustomException(detail="User is not a Customer", status_code=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                raise CustomException(detail="User does not exist", status_code=status.HTTP_404_NOT_FOUND)
        else:
            raise CustomException(detail="Invalid user id", status_code=status.HTTP_400_BAD_REQUEST)

    
