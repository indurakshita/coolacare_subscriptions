from django.contrib import admin
from django.apps import apps


app = apps.get_app_config("confapp")

models = app.get_models()
for model in models:
    admin.site.register(model)
