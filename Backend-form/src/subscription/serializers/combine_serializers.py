from rest_framework import serializers
from subscription.serializers.status_serializers import ScheduleStatusSerializer
from subscription.models.schedule_model_call import SubscriptionScheduleCall
from subscription.models.subscription_model import Subscription
from subscription.models.status_model import ScheduleStatus
from subscription.models.avaialbleslots import AvailableSlots


class CombineSlotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableSlots
        fields = ['day', 'daytime', 'time']


class CombineScheduleSerializer(serializers.ModelSerializer):
    statuses = ScheduleStatusSerializer(many=True, read_only=True)
    available_slot = CombineSlotsSerializer(read_only=True)
    subscriptionScheduleId = serializers.IntegerField(source='id')
    day = serializers.CharField(source='avaialbleslote.day')
    daytime = serializers.CharField(source='avaialbleslote.daytime')
    time = serializers.CharField(source='avaialbleslote.time')

    class Meta:
        model = SubscriptionScheduleCall
        fields = ['subscriptionScheduleId','subscription_id', 'feedback', 'agent_user_id', 'scheduled_date', 'start_time', 'end_time', 'day', 'daytime', 'time', 'statuses','available_slot']



class CombineSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class CombineStatusSerializer(serializers.ModelSerializer):
    status_id = serializers.ReadOnlyField(source='id')
    class Meta:
        model = ScheduleStatus
        fields = ['status_id', 'status','timestamp']