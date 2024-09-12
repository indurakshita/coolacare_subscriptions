from django.db import models
from subscription.models.subscription_model import Subscription
from subscription.models.avaialbleslots import AvailableSlots


class SubscriptionScheduleCall(models.Model):
    id = models.BigAutoField(primary_key=True)
    subscription_id = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    feedback = models.TextField(blank=True, null=True)
    agent_user_id = models.IntegerField(blank=True, null=True)
    scheduled_date = models.DateField()
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    avaialbleslote = models.ForeignKey(AvailableSlots, on_delete=models.CASCADE)
    
    
    def save(self, *args, **kwargs):
        if not self.pk:
            subscription_id = self.subscription_id.id
            call = "0"
            last_schedule = SubscriptionScheduleCall.objects.order_by('-id').first()
            if last_schedule:
                schedule_id = int(last_schedule.id) + 1
                self.id = schedule_id
            else:
                schedule_id = 1
                custom_id = f"{subscription_id}{call}{str(schedule_id).zfill(5)}"
                self.id = int(custom_id)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subscription_id}-{self.scheduled_date}"


