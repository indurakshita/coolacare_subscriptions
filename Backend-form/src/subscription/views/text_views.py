from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from subscription.models.schedule_model_text import SubscriptionScheduleText
from subscription.serializers.text_serializer import SubscriptionScheduleTextSerializer
from authapp.exception import CustomException
from authapp.permissions.group_permission import HasGroupPermission
from authapp.authentication import JWTAuthenticationBackend
from authapp.validate.validation import validate_response



class TextAPIView(APIView):
    authentication_classes = [JWTAuthenticationBackend]
    model_name = 'SubscriptionScheduleText'.lower()
    permission_classes = [HasGroupPermission]


    def get(self, request):
        subscription_id = request.data.get('subscription_id',None)
        day = request.data.get('day',None)
        time = request.data.get('time',None)
        daytime = request.data.get('daytime',None)
        if not subscription_id:
            if request.user.groups.filter(name__in=["Admin", "ProviderAdmin"]).exists():
                text = SubscriptionScheduleText.objects.all()
                serializer = SubscriptionScheduleTextSerializer(text, many=True)
                return Response(serializer.data)
            else:
                return Response([],status=200)
        
        else:
            try:
                filter_criteria = {"subscription_id":subscription_id}
                if day:
                    filter_criteria['day']=day
                if daytime:
                    filter_criteria['daytime']=daytime
                if time:
                    filter_criteria['time']=time
                
                # status_subquery = ScheduleStatus.objects.filter(id=OuterRef('id')).values('status')[:1]
                filtered_data = SubscriptionScheduleText.objects.filter(**filter_criteria)

                serializer = SubscriptionScheduleTextSerializer(filtered_data, many=True)
                if serializer.data:
                    return Response(serializer.data)
                else:
                    return Response([],status=200)
                
            except SubscriptionScheduleText.DoesNotExist:
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