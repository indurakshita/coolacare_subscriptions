from rest_framework import serializers
from confapp.models.conf_model import Configuration

class ConfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuration
        fields = '__all__'