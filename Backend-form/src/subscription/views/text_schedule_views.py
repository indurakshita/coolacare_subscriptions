from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from subscription.models.schedule_model_text import SubscriptionScheduleText
from subscription.serializers.text_serializer import SubscriptionScheduleTextSerializer, SubscriptionTextSerializer
from authapp.exception import CustomException
from authapp.permissions.group_permission import HasGroupPermission
from authapp.authentication import JWTAuthenticationBackend
from authapp.validate.validation import validate_response
from datetime import datetime, timedelta, date
from django.contrib.auth import get_user_model
from subscription.utils.hours_converter import convert_time_edt_txt
from django.db.models import Q

User = get_user_model()


class TextAPIView(APIView):
    authentication_classes = [JWTAuthenticationBackend]
    model_name = 'SubscriptionScheduleText'.lower()
    permission_classes = [HasGroupPermission]

    def get(self, request):
        subscription_id = request.query_params.get('subscription_id')
        day = request.query_params.get('day')
        time = request.query_params.get('time')
        daytime = request.query_params.get('daytime')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        phone_number = request.query_params.get('phone_number')
        status = request.query_params.get('status')

        filter_criteria= {}
        if subscription_id:
            filter_criteria['subscription_id'] = subscription_id
        if day:
            filter_criteria['day__icontains'] = day
        if daytime:
            filter_criteria['daytime__icontains'] = daytime
        if time:
            filter_criteria['time'] = time
        if phone_number:
            filter_criteria['subscription_id__phone__icontains'] = phone_number

        groups = User.objects.filter(id=request.user.id).values_list('groups__name', flat=True)
        current_date = date.today()
        if 'Admin' in groups or 'ProviderAdmin' in groups:
            if date_from and date_to:
                filter_criteria['date__range'] = [date_from, date_to]
            elif date_from:
                date_to = datetime.strptime(date_from, "%Y-%m-%d") + timedelta(days=7)
                filter_criteria['date__range'] = [date_from, date_to]
            elif date_to:
                date_from = datetime.strptime(date_to, "%Y-%m-%d") - timedelta(days=7)
                filter_criteria['date__range'] = [date_from, date_to]
            else:
                filter_criteria['date'] = current_date

        elif 'Customer' in groups:
            future_date = current_date + timedelta(days=30)
            filter_criteria['date__gte'] = current_date
            filter_criteria['date__lte'] = future_date
            
        if filter_criteria:
            all_filters = Q(**filter_criteria)        
            filtered_data = SubscriptionScheduleText.objects.filter(all_filters)
            serializer = SubscriptionTextSerializer(filtered_data, many=True)
            if serializer.data:
                serialized_data = [{
                    **item,
                    'time': convert_time_edt_txt(item['time'])  # Assuming 'time' is the key for the time field
                } for item in serializer.data]

                if status:
                    filtered_data = [item for item in serialized_data if item.get('status') == status]
                    return Response(filtered_data, status=200)
                return Response(serialized_data, status=200)
        return Response([],status=200)

    def put(self, request):
        try:
            pk = request.data.get('id')
            if not pk:
                return validate_response("TextIdInvalid")
            instance = SubscriptionScheduleText.objects.get(pk=pk)
        except SubscriptionScheduleText.DoesNotExist:
            return validate_response("TextNotFound")

        serializer = SubscriptionScheduleTextSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return validate_response("TextUpdated")
        else:
            error = [f"{field} {error}" for field, errors in serializer.errors.items() for error in errors][0]
            raise CustomException(detail=error, status_code=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            pk = request.data.get('id')
            if not pk:
                return validate_response("TextIdInvalid")
            instance = SubscriptionScheduleText.objects.get(pk=pk)
            instance.delete()
            return validate_response("TextDeleted")
        except SubscriptionScheduleText.DoesNotExist:
            return validate_response("TextNotFound")