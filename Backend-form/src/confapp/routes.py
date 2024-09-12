from rest_framework.routers import DefaultRouter
from django.urls import path, include
from confapp.views.lable_view import UILabelViewSet
from confapp.views.conf_view import ConfViewset

router = DefaultRouter()
router.register(r'ui-labels', UILabelViewSet)
router.register(r"configurations",ConfViewset)

