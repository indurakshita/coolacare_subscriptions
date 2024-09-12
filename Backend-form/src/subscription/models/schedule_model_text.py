from django.db import models
from subscription.models.subscription_model import Subscription
from icecream import ic

class SubscriptionScheduleText(models.Model):
    id = models.BigAutoField(primary_key=True)
    subscription_id = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    schedule_status_id = models.IntegerField()
    date = models.DateField()
    day = models.CharField(max_length=255)
    daytime = models.CharField(max_length=255)
    time = models.CharField(max_length=255)

    
    def save(self, *args, **kwargs):
        if not self.pk:
            subscription_id = self.subscription_id.id
            call = "1"
            last_schedule = SubscriptionScheduleText.objects.order_by('-id').first()
            if last_schedule:
                schedule_id = int(last_schedule.id) + 1
                self.id = int(schedule_id)
            else:
                schedule_id = 1
                custom_id = f"{subscription_id}{call}{str(schedule_id).zfill(5)}"
                self.id = int(custom_id)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subscription_id}-{self.date}"