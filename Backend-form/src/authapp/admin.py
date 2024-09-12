from django.contrib import admin
from django.apps import apps
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

app = apps.get_app_config("authapp")

admin.site.register(Permission)
admin.site.register(ContentType)
models = app.get_models()
for model in models:
    
    admin.site.register(model)
