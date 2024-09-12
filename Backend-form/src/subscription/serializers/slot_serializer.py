from rest_framework import serializers
from subscription.models.avaialbleslots import AvailableSlots
from rest_framework import serializers
from subscription.models.schedule_model_text import SubscriptionScheduleText


class AvailableSlotsSerializer(serializers.ModelSerializer):
    day = serializers.CharField(required=True)
    daytime = serializers.CharField(required=False)
    time = serializers.CharField(required=False)
    total_slots = serializers.IntegerField(required=True)
    booked_slots = serializers.IntegerField(required=True)
    available_slots = serializers.IntegerField(required=False)
    
    class Meta:
        model = AvailableSlots
        fields = ['id', 'day', 'daytime', 'time', 'total_slots', 'booked_slots', 'available_slots']



class SubscriptionScheduleTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionScheduleText
        fields = ['id', 'subscription_id', 'schedule_status_id', 'date', 'day', 'daytime', 'time']


class GroupedAvailableSlotsSerializer(serializers.Serializer):
    daytime = serializers.CharField()
    available_slots = serializers.IntegerField()
    time = serializers.CharField()

    class Meta:
        fields = ['daytime', 'time', 'available_slots']
