from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from subscription.models.schedule_model_call import SubscriptionScheduleCall
from subscription.serializers.schedule_serializer import SubscriptionScheduleSerializer
from authapp.exception import CustomException
from authapp.permissions.group_permission import HasGroupPermission
from authapp.authentication import JWTAuthenticationBackend
from authapp.validate.validation import validate_response
from datetime import date
from subscription.models.status_model import ScheduleStatus


class SubscriptionScheduleAPIView(APIView):
    authentication_classes = [JWTAuthenticationBackend]
    model_name = 'SubscriptionScheduleCall'.lower()
    permission_classes = [HasGroupPermission]
    serializer_class = SubscriptionScheduleSerializer

    def get(self, request, pk=None):
        if not pk:  # Check if the ID is '1'
            if request.user.groups.filter(name__in=["Admin", "ProviderAdmin"]).exists():
                subscriptions = SubscriptionScheduleCall.objects.all()
                serializer = self.serializer_class(subscriptions, many=True)
                return Response(serializer.data)
            elif request.user.groups.filter(name="Agent").exists():
                subscriptions = SubscriptionScheduleCall.objects.filter(scheduled_date=date.today())
                serializer = self.serializer_class(subscriptions, many=True)
                return Response(serializer.data)
            else:
                return validate_response("ScheduleNotFound")
        else:
            try:
                filtered_data = SubscriptionScheduleCall.objects.filter(subscription_id__created_by_id=request.user.id,id=pk)
                serializer = self.serializer_class(filtered_data, many=True)
                return Response(serializer.data)
            except SubscriptionScheduleCall.DoesNotExist:
                return validate_response("ScheduleNotFound")

    def post(self, request):
        serializer = self.serializer_class(data=request.data)        
        if serializer.is_valid():
            agent_user_id = serializer.validated_data.get('agent_user_id')
            scheduled_date = serializer.validated_data.get('scheduled_date')
            start_time = serializer.validated_data.get('start_time')
            end_time = serializer.validated_data.get('end_time')
            daytime = serializer.validated_data.get('daytime')
            if SubscriptionScheduleCall.objects.filter(agent_user_id=agent_user_id, scheduled_date=scheduled_date,\
                                                    start_time=start_time, end_time=end_time, daytime=daytime).exists():
                return validate_response("ScheduleAlreadyExist")
            serializer.save()
            return validate_response("ScheduleCreated")
        else:
            error = [f"{field} {error}" for field, errors in serializer.errors.items() for error in errors][0]
            raise CustomException(detail=error, status_code=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            pk = request.data.get('subscription_schedule_id')
            if not pk:
                return validate_response("ScheduleIdInvalid")
            instance = SubscriptionScheduleCall.objects.get(pk=pk)
            instance.agent_user_id = request.user.id
            status_instance = ScheduleStatus.objects.get(callschedule_id=instance)
            status_instance.status = "COMPLETED"
            status_instance.save()
        except SubscriptionScheduleCall.DoesNotExist:
            return validate_response("ScheduleNotFound")

        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return validate_response("ScheduleUpdate")
        else:
            error = [f"{field} {error}" for field, errors in serializer.errors.items() for error in errors][0]
            raise CustomException(detail=error, status_code=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            pk = request.data.get('subscription_schedule_id')
            if not pk:
                return validate_response("ScheduleIdInvalid")
            instance = SubscriptionScheduleCall.objects.get(pk=pk)
            instance.delete()
            return validate_response("ScheduleDeleted")
        except SubscriptionScheduleCall.DoesNotExist:
            return validate_response("ScheduleNotFound")
