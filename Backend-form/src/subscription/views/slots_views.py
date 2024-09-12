from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from subscription.models.avaialbleslots import AvailableSlots
from subscription.serializers.slot_serializer import AvailableSlotsSerializer, GroupedAvailableSlotsSerializer
from authapp.exception import CustomException
from authapp.permissions.group_permission import HasGroupPermission
from authapp.authentication import JWTAuthenticationBackend
from authapp.validate.validation import validate_response
from django.db.models import Min
from datetime import datetime


def convert_to_12_hours(time_range_str):
    start_time, end_time = time_range_str.split(" - ")
    start_time_obj = datetime.strptime(start_time, '%H:%M')
    end_time_obj = datetime.strptime(end_time, '%H:%M')
    return f"{start_time_obj.strftime('%I:%M %p')} - {end_time_obj.strftime('%I:%M %p')}"


class AvailableSlotsAPIView(APIView):
    authentication_classes = [JWTAuthenticationBackend]
    model_name = 'AvailableSlots'.lower()
    permission_classes = [HasGroupPermission]


    def get(self, request, pk=None):
        if not pk:
            instances = AvailableSlots.objects.all()
            if not instances:
                return Response([],status=200)
            least_available = instances.values('daytime','time').annotate(available_slots=Min('available_slots'))
            for slot in least_available:
                slot['time'] = convert_to_12_hours(slot['time'])
            serializer = GroupedAvailableSlotsSerializer(least_available, many=True)
            return Response(serializer.data)
        else:
            try:
                instance = AvailableSlots.objects.get(pk=pk)
                serializer = AvailableSlotsSerializer(instance)
                return Response(serializer.data)
            except AvailableSlots.DoesNotExist:
                return Response([],status=200)

    def post(self, request):
        serializer = AvailableSlotsSerializer(data=request.data)        
        if serializer.is_valid():
            day = serializer.validated_data.get('day')
            daytime = serializer.validated_data.get('daytime')
            if AvailableSlots.objects.filter(day=day, daytime=daytime).exists():
                return validate_response("SlotAlreadyExist")
            serializer.save()
            return validate_response("SlotCreated")
        else:
            error = [f"{field} {error}" for field, errors in serializer.errors.items() for error in errors][0]
            raise CustomException(detail=error, status_code=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            pk = request.data.get('id')
            if not pk:
                return validate_response("SlotIdInvalid")
            instance = AvailableSlots.objects.get(pk=pk)
        except AvailableSlots.DoesNotExist:
                return validate_response("SlotNotFound")
        serializer = AvailableSlotsSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return validate_response("SlotUpdate")
        else:
            error = [f"{field} {error}" for field, errors in serializer.errors.items() for error in errors][0]
            raise CustomException(detail=error, status_code=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            pk = request.data.get('id')
            if not pk:
                return validate_response("SlotIdInvalid")
            instance = AvailableSlots.objects.get(pk=pk)
            instance.delete()
            return validate_response("SlotDeleted")
        except AvailableSlots.DoesNotExist:
            return validate_response("SlotNotFound")