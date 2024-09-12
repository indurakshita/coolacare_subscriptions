from rest_framework import serializers


class PaymentConfirmationSerializer(serializers.Serializer):
    sessionid = serializers.CharField()


class RefundSerializer(serializers.Serializer):
    intent_id = serializers.CharField()
