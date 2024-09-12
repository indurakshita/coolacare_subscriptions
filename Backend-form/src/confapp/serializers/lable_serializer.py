from rest_framework import serializers
from confapp.models.lable_model import UILabel

class UILabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UILabel
        fields = '__all__'