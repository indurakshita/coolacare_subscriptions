from django.core.management.base import BaseCommand
from django.utils import timezone
from django_q.tasks import schedule, Schedule

class Command(BaseCommand):
    help = 'Schedule a monthly task'

    def handle(self, *args, **options):
        next_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0) + timezone.timedelta(days=32)
        next_month = next_month.replace(day=1)

        existing_schedule = Schedule.objects.filter(func='subscription.schedule_tasks.my_monthly_task').exists()
        if existing_schedule:
            Schedule.objects.filter(func='subscription.schedule_tasks.my_monthly_task').delete()

        schedule('subscription.schedule_tasks.my_monthly_task',
                 schedule_type=Schedule.MONTHLY,
                 next_run=next_month,
                 repeats=0)
        self.stdout.write(self.style.SUCCESS('Task scheduled to run monthly on the 1st'))