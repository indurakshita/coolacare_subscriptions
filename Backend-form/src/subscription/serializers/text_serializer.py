from subscription.models.schedule_model_text import SubscriptionScheduleText
from subscription.serializers.subscription_serializer import SubscriptionSerializer

from rest_framework import serializers

class SubscriptionScheduleTextSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return obj.schedulestatus_set.first().status if obj.schedulestatus_set.exists() else None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['status'] = self.get_status(instance)
        return representation
    
    class Meta:
        model = SubscriptionScheduleText
        fields = "__all__"

class SubscriptionTextSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    subscription_id = SubscriptionSerializer()

    def get_status(self, obj):
        return obj.text_status.first().status if obj.text_status.exists() else None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['status'] = self.get_status(instance)
        return representation
    
    class Meta:
        model = SubscriptionScheduleText
        fields = "__all__"