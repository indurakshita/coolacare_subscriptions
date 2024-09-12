from subscription.models.subscription_model import Subscription
from subscription.serializers.subscription_serializer import SubscriptionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from subscription.models import Subscription
from authapp.exception import CustomException
from authapp.authentication import JWTAuthenticationBackend
from datetime import datetime, timedelta
from authapp.validate.validation import validate_response
from subscription.models.slote_model import Slots
from subscription.models.avaialbleslots import AvailableSlots
from django.db.models import Min
from django.db.models import Q
from authapp.permissions.group_permission import HasGroupPermission
from django.shortcuts import get_object_or_404
from rest_framework import status
from subscription.serializers.subscription_validation import SubscriptionValidationSerializer
from subscription.utils.hours_converter import convert_to_24_hours




class SubscriptionAPIView(APIView):
    authentication_classes = [JWTAuthenticationBackend]
    model_name = 'Subscription'.lower()
    permission_classes = [HasGroupPermission]
   
    def get(self, request, pk=None):
        if not pk:  # Check if the ID is '1'
            if request.user.groups.filter(name__in=["Admin", "ProviderAdmin"]).exists():  # Check if user is in the Admin group
                subscriptions = Subscription.objects.all().order_by('-created_at')
                serializer = SubscriptionSerializer(subscriptions, many=True)
                return Response(serializer.data)
            else:
                subscriptions = Subscription.objects.filter(created_by=request.user).order_by('-created_at')
                serializer = SubscriptionSerializer(subscriptions, many=True)
                return Response(serializer.data)
        else:
            try:
                subscription = Subscription.objects.get(pk=pk)
                serializer = SubscriptionSerializer(subscription)
                return Response(serializer.data)
            except Subscription.DoesNotExist:
                return Response([],status=200)

    def post(self, request):
    
        user_id = request.user.id
        if request.data["package"] == "GOLD":
            least_available = AvailableSlots.objects.values('daytime', 'time').annotate(
                available_slots=Min('available_slots')
            ).filter(
                available_slots__gt=0
            )
            if not least_available.exists():
                raise CustomException(detail="Slotes are booked cantact our support team",status_code=400)

        request.data['created_by'] = user_id
        plan = request.data.get("plan",None)


        if plan is None or plan not in ["YEARLY", "MONTHLY"]:
            raise CustomException(detail="Invalid plan value", status_code=status.HTTP_400_BAD_REQUEST)
        
        subscription = Subscription.objects.filter(created_by=request.user).first()
        plan_durations = {
            "YEARLY": timedelta(days=365) if subscription else timedelta(days=365+30),
            "MONTHLY": timedelta(days=30) if subscription else timedelta(days=30+30)
        }
        start_date = datetime.now() + timedelta(days=2)
        end_date = start_date + plan_durations[plan]

        request.data['start_date'] = start_date.strftime("%Y-%m-%d")
        request.data['end_date'] = end_date.strftime("%Y-%m-%d")
        serializer = SubscriptionSerializer(data=request.data)
        required_fields = {
            'dayname': request.data.get('dayname'),
            'session': request.data.get('session'),
            'time': request.data.get('time'),
            'mode_of_call': request.data.get('mode_of_call'),
            "package":request.data.get('package')
        }
        
        if serializer.is_valid():
            if serializer.validated_data.get("package")=="SILVER" and serializer.validated_data.get("mode_of_call")=="VOICE":
                raise CustomException(detail="Silver user don't have voice option", status_code=400)
            validation_serializer = SubscriptionValidationSerializer(data=required_fields)
            if validation_serializer.is_valid():
                instance  = serializer.save(created_by_id=user_id) 
                Slots.objects.create(
                    subscription=instance,
                    dayname=request.data.get('dayname'),
                    session=request.data.get('session'),
                    time=convert_to_24_hours(request.data.get('time')) if serializer.validated_data.get("mode_of_call")=="VOICE" else request.data.get('time'),
                    trial = False if subscription else True,
                )
                data = serializer.data
                response_data = {"data": data, "code": 201}
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                error_message = [f"{field}: {error}" for field, errors in serializer.errors.items() for error in errors][0]
                raise CustomException(detail=error_message, status_code=400)
        else:
            error_message = [f"{field}: {error}" for field, errors in serializer.errors.items() for error in errors][0]
            raise CustomException(detail=error_message, status_code=400)
        
        
    def put(self, request):
        pk = request.data.get('id')
        if pk is None:
            raise CustomException(detail="ID is required in the request body for updating a subscription")
        subscription = get_object_or_404(Subscription, pk=pk)
        serializer = SubscriptionSerializer(subscription, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return validate_response("SubscriptionUpdated")
        else:
            error_message = [f"{field}: {error}" for field, errors in serializer.errors.items() for error in errors][0]
            raise CustomException(detail=error_message, status_code=400)

    def delete(self, request):
        pk = request.data.get('id')
        if pk is None:
            raise CustomException(detail="ID is required in the request body for deleting a subscription")

        subscription = get_object_or_404(Subscription, pk=pk)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


