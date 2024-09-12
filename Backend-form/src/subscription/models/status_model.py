from django.db import models
from subscription.models.schedule_model_call import SubscriptionScheduleCall
from subscription.models.schedule_model_text import SubscriptionScheduleText

class ScheduleStatus(models.Model):
    STATUS_CHOICES = (
        ("SCHEDULED", "Scheduled"),
        ("MISSED", "Missed"),
        ("VOICE_MAIL", "Voice Mail"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
    )
    id = models.AutoField(primary_key=True)
    callschedule_id = models.ForeignKey(SubscriptionScheduleCall, on_delete=models.CASCADE,null=True,related_name='statuses')
    textschedule_id = models.ForeignKey(SubscriptionScheduleText, on_delete=models.CASCADE,null=True,related_name='text_status')
    status = models.CharField(max_length=255,choices=STATUS_CHOICES,default="SCHEDULED")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Status for Subscription Schedule {self.status}"
