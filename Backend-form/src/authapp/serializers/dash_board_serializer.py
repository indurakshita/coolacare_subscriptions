from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","email", "is_active","first_name","last_name","street_address","city","postal_code","country"]
    
class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","email", "is_active",'is_provideradmin']