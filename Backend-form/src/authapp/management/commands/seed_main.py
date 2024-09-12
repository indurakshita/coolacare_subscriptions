from django.core.management import call_command
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command('seed_val')
        # call_command('seed_group')
        # call_command('seed_conf')
        # call_command("seed_slot")
        # call_command("seed_uilable")
        # call_command("seed_permission_admin")
        # call_command("seed_permission_agent")
        # call_command("seed_permission_customer")
        # call_command("seed_permission_provideradmin")
        # call_command("daily_schedule")
        call_command("monthly_schedule")
        pass