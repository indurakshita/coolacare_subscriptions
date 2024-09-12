from django.utils import timezone
from .models.subscription_model import Subscription


from django.utils import timezone
from .models import Subscription

def my_daily_task():
    now = timezone.now().date()
    subscriptions = Subscription.objects.all()
    for sub in subscriptions:
        if sub and sub.status != "CANCELED" and sub.status != "ON HOLD" :
            if sub.start_date <= now < sub.end_date:
                sub.status = 'ACTIVE'
                print(f"Status updated for {sub} to {sub.status}")
            elif now >= sub.end_date:
                sub.status = 'EXPIRED'
                print(f"Status updated for {sub} to {sub.status}")

    # Update the status for all subscriptions in bulk
    Subscription.objects.bulk_update(subscriptions, ['status'])

    
def my_monthly_task():
    now = timezone.now().date()
    subscriptions = Subscription.objects.filter(status="ON HOLD")
    for sub in subscriptions:
        sub.delete()
        print(f"Subscription {sub.id} deleted")

    