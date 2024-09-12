from django.urls import path, include
from confapp.routes import router


urlpatterns = [
    path("", include(router.urls), name="confapp"),
]
