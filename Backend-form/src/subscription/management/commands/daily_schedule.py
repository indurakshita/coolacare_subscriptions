# myapp/management/commands/schedule_daily_task.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from django_q.tasks import schedule, Schedule

class Command(BaseCommand):
    help = 'Schedule a daily task'

    def handle(self, *args, **options):
        tomorrow_midnight = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)

        existing_schedule = Schedule.objects.filter(func='subscription.schedule_tasks.my_daily_task').exists()
        if existing_schedule:
            # If the task is already scheduled, remove the existing schedule
            Schedule.objects.filter(func='subscription.schedule_tasks.my_daily_task').delete()

        # Schedule the task to run daily at midnight
        schedule('subscription.schedule_tasks.my_daily_task',
                 schedule_type=Schedule.DAILY,
                 next_run=tomorrow_midnight,
                 repeats=0)  # Specify repeats=0 for an indefinite daily schedule
        self.stdout.write(self.style.SUCCESS('Task scheduled to run daily at midnight'))

