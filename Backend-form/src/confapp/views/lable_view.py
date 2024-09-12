from rest_framework import viewsets
from confapp.models.lable_model import UILabel
from confapp.serializers.lable_serializer import UILabelSerializer

class UILabelViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    queryset = UILabel.objects.all()
    serializer_class = UILabelSerializer
