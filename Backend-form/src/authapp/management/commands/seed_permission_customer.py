from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.apps import apps
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Assign permissions based on model names to a group'

    def find_app_label(self, model_name):
        for app_config in apps.get_app_configs():
            for model in app_config.get_models():
                if model.__name__ == model_name:
                    return app_config.label
        return None

    def handle(self, *args, **kwargs):
        group_name = 'Customer'  # Replace 'Customer' with your actual group name

        model_permissions = {
            'Subscription': ['add', 'change', 'delete', 'view'],
            "ApiLabel":['view'],
            "UILabel":['view'],
            "CustomUser":["view",'change'],
            "Payment":["view","add"],
            "ScheduleStatus":["view"],
            "SubscriptionScheduleCall":["view"],
            "SubscriptionScheduleText":["view"],
            "AvailableSlots":["view"],
           
        }

        for model_name, permissions in model_permissions.items():
            app_label = self.find_app_label(model_name)

            if app_label:
                content_type = ContentType.objects.get(app_label=app_label, model=model_name.lower())
                for permission_type in permissions:
                    codename = f"{permission_type}_{model_name.lower()}"
                    permission, created = Permission.objects.get_or_create(
                        codename=codename,
                        content_type=content_type
                    )
                    group, created = Group.objects.get_or_create(name=group_name)
                    group.permissions.add(permission)
                    self.stdout.write(self.style.SUCCESS(f"Added permission '{codename}' to group '{group_name}' for model '{model_name}'"))
            else:
                self.stdout.write(self.style.ERROR(f"Model '{model_name}' not found"))
