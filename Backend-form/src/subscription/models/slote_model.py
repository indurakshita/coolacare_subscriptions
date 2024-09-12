from django.db import models
from subscription.models import Subscription

class Slots(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    dayname = models.JSONField(default=list)  # Store day names as JSON array
    session = models.JSONField(default=list)  # Store sessions as JSON array
    time = models.JSONField(default=list)  # Store times as JSON array
    booked = models.BooleanField(default=False)
    trial = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.dayname} - {self.session} - {self.time}"