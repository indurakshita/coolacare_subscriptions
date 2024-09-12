from django.apps import AppConfig
from django.conf import settings

class AuthappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authapp'
    def ready(self):
        from confapp.models.conf_model import Configuration
        try:
            email_config = Configuration.objects.first()
            if email_config:
                settings.EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
                settings.EMAIL_HOST = Configuration.objects.get(key="host").value
                settings.EMAIL_PORT = Configuration.objects.get(key="port").value
                settings.EMAIL_HOST_USER = Configuration.objects.get(key="email").value
                settings.EMAIL_HOST_PASSWORD = Configuration.objects.get(key="password").value
                settings.EMAIL_USE_TLS = True
                
        except Exception as e:
            pass
        
