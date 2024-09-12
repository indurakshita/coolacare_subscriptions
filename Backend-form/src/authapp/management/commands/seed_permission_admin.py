from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Add all permissions to the admin group'

    def handle(self, *args, **kwargs):
        # Get or create the admin group
        admin_group, created = Group.objects.get_or_create(name='Admin')

        # Get all permissions
        all_permissions = Permission.objects.all()

        # Add all permissions to the admin group
        admin_group.permissions.set(all_permissions)

        self.stdout.write(self.style.SUCCESS('Successfully added all permissions to the admin group'))
