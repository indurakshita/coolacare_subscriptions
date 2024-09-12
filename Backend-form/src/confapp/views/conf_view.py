from rest_framework import viewsets
from confapp.models.conf_model import Configuration
from confapp.serializers.conf_serializer import ConfSerializer

class ConfViewset(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    queryset = Configuration.objects.all()
    serializer_class = ConfSerializer