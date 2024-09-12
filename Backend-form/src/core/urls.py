from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
   SpectacularAPIView,SpectacularSwaggerView,SpectacularRedocView
)

urlpatterns = [
   path('yaml/', SpectacularAPIView.as_view(), name='schema'),
   path('readoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
   path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
   path("admin/", admin.site.urls),
   path("common/", include("common.urls")),
   path("auth/", include("authapp.urls")),
   path("config/", include("confapp.urls")),
   path("subscription/", include("subscription.urls")),

   
]

