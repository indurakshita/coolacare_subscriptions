from django.db import models

class ApiLabel(models.Model):
    MESSAGE_TYPE_CHOICES = [
        ('Error', 'Error'),
        ('Success', 'Success'),
    ]
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES)
    label = models.CharField(max_length=255)
    message = models.TextField()
    action = models.CharField(max_length=20)
    status_code = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.label} ({self.type})"

