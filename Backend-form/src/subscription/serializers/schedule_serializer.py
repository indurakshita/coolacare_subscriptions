from rest_framework import serializers
from subscription.models.schedule_model_call import SubscriptionScheduleCall
from subscription.models.subscription_model import Subscription
from subscription.models.avaialbleslots import AvailableSlots

class SubscriptionScheduleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    subscription_id = serializers.PrimaryKeyRelatedField(queryset=Subscription.objects.all(), required=True)
    feedback = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    agent_user_id = serializers.IntegerField(required=True, allow_null=True)
    scheduled_date = serializers.DateField(required=False, allow_null=True)
    start_time = serializers.TimeField(required=False, allow_null=True)
    end_time = serializers.TimeField(required=False, allow_null=True)
    avaialbleslote = serializers.PrimaryKeyRelatedField(queryset=AvailableSlots.objects.all(), required=True)

    class Meta:
        model = SubscriptionScheduleCall
        fields = ['id','subscription_id', 'feedback', 'agent_user_id',
                   'scheduled_date', 'start_time', 'end_time', "avaialbleslote"]
