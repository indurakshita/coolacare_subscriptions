from rest_framework import serializers
from subscription.models.status_model import ScheduleStatus
from subscription.models.schedule_model_call import SubscriptionScheduleCall

class ScheduleStatusSerializer(serializers.ModelSerializer):
    status_id = serializers.IntegerField(source="id")    
    class Meta:
        model = ScheduleStatus
        fields = ['status_id','status','timestamp']
