from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from subscription.models.status_model import ScheduleStatus
from subscription.serializers.status_serializers import ScheduleStatusSerializer
from authapp.exception import CustomException
from authapp.permissions.group_permission import HasGroupPermission
from authapp.authentication import JWTAuthenticationBackend
from authapp.validate.validation import validate_response

class StatusAPIView(APIView):
    authentication_classes = [JWTAuthenticationBackend]
    model_name = 'ScheduleStatus'.lower()
    permission_classes = [HasGroupPermission]
    serializer_class = ScheduleStatusSerializer

    def get(self, request, pk=None):
        if not pk:
            instances = ScheduleStatus.objects.all()
            if not instances:
                return Response([],status=200)
            serializer = self.serializer_class(instances, many=True)
            return Response(serializer.data)
        else:
            try:
                instance = ScheduleStatus.objects.get(pk=pk)
                serializer = self.serializer_class(instance)
                return Response(serializer.data)
            except ScheduleStatus.DoesNotExist:
                return Response([],status=200)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)        
        if serializer.is_valid():
            # ssid = serializer.validated_data.get('subscription_schedule_id')
            # status = serializer.validated_data.get('status')

            # if ScheduleStatus.objects.filter(day=day, daytime=daytime).exists():
            #     raise CustomException(detail="Status already exists", status_code=status.HTTP_409_CONFLICT)
            serializer.save()
            return validate_response("StatusCreated")
        else:
            error = [f"{field} {error}" for field, errors in serializer.errors.items() for error in errors][0]
            raise CustomException(detail=error, status_code=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            pk = request.data.get('id')
            if not pk:
                return validate_response("StatusIdInvalid")
            instance = ScheduleStatus.objects.get(pk=pk)
        except ScheduleStatus.DoesNotExist:
            return validate_response("StatusNotFound")

        serializer = self.serializer_class(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return validate_response("StatusUpdate")
        else:
            error = [f"{field} {error}" for field, errors in serializer.errors.items() for error in errors][0]
            raise CustomException(detail=error, status_code=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            pk = request.data.get('id')
            if not pk:
                return validate_response("StatusIdInvalid")
            instance = ScheduleStatus.objects.get(pk=pk)
            instance.delete()
            return validate_response("StatusDeleted")
        except ScheduleStatus.DoesNotExist:
            return validate_response("StatusNotFound")