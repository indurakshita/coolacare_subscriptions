from django.db import models
from datetime import date ,timedelta
from authapp.models.authmodel import CustomUser
from django.utils import timezone

class Subscription(models.Model):
    PACKAGE_CHOICES = [
        ('SILVER', 'Silver'),
        ('GOLD', 'Gold'),
        ('PLATINUM', 'Platinum'),
    ]

    MODE_OF_CALL_CHOICES = [
        ('SMS', 'SMS'),
        ('VOICE', 'VOICE'),
    ]

    TYPE_OF_CALL_CHOICES = [
        ('COURTESY_CALLS', 'COURTESY_CALLS'),
        ('WELLNESS_CALLS', 'WELLNESS_CALLS'),
        ('PHONE_A_FRIEND', 'PHONE_A_FRIEND'),
        ('MEDICATION_REMINDERS_CALL', 'MEDICATION_REMINDERS_CALL'),
        ('MEAL_REMINDER_CALL', 'MEAL_REMINDER_CALL'),
        ('COURTESY_TEXT', 'COURTESY_TEXT'),
        ('WELLNESS_TEXT', 'WELLNESS_TEXT'),
        ('TEXT_A_FRIEND', 'TEXT_A_FRIEND'),
        ('MEDICATION_REMINDERS_TEXT', 'MEDICATION_REMINDERS_TEXT'),
        ('MEAL_REMINDER_TEXT', 'MEAL_REMINDER_TEXT'),
    ]
    PLAN_CHOICES = [
        ('MONTHLY', 'Monthly'),
        ('YEARLY', 'Yearly'),
    ]
    STATUS_CHOICES = [
        ('ON HOLD', 'ON HOLD'),
        ('CREATED', 'CREATED'),
        ('ACTIVE', 'ACTIVE'),
        ('EXPIRED', 'EXPIRED'),
        ('CANCELLED', 'CANCELLED'),
    ]

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255,null=True)
    last_name = models.CharField(max_length=255,null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    package = models.CharField(max_length=255, choices=PACKAGE_CHOICES)
    plan = models.CharField(max_length=7,choices=PLAN_CHOICES,default=None,null=True)
    start_date = models.DateField(null=True,default=(date.today() + timedelta(days=2)))
    end_date = models.DateField(null=True)
    type_of_call = models.CharField(max_length=255, choices=TYPE_OF_CALL_CHOICES)
    mode_of_call = models.CharField(max_length=255, choices=MODE_OF_CALL_CHOICES)
    communication_email = models.EmailField()
    alternate_contact = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255,choices=STATUS_CHOICES ,default="ON HOLD")
    acknowledgement = models.BooleanField(default=False)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,default=None)
    message = models.CharField(max_length=1000, blank=True, null=True, default="")
    trial = models.BooleanField(default=False)
    created_at = models.DateField(null=True,default=date.today)

    
    def save(self, *args, **kwargs):
        if not self.id:
            current_year = str(timezone.now().year)[-2:]  # Get the last two digits of the current year
            current_month = str(timezone.now().month).zfill(2)  # Get the current month as a zero-padded string
            last_subscription = Subscription.objects.order_by('-id').first()
            last_id = int(str(last_subscription.id)[-4:]) if last_subscription else 0
            next_id = last_id + 1
            self.id = f"{current_year}{current_month}{str(next_id).zfill(4)}"
        super().save(*args, **kwargs)


    def __str__(self):
        return self.package

