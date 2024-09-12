from django.db import models
from subscription.models.subscription_model import Subscription

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    payment_confirmation= models.CharField(max_length=225)
    payment_indent_id = models.CharField(max_length=512)
    subscription_id = models.ForeignKey(Subscription, on_delete=models.CASCADE)

    def __str__(self):
        return f"Payment ID: {self.id}"