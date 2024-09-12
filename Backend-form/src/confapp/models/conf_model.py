from django.db import models


class Configuration(models.Model):
    id = models.AutoField(primary_key=True)
    config_type = models.CharField(max_length=20)
    key = models.CharField(max_length=255, default="")
    value = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.config_type}"