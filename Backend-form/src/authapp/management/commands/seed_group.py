from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from pathlib import Path
import json

base = Path(__file__).parent.parent
filepath = base / "json/groups.json"

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open(filepath) as f:
            data = json.load(f)

        for item in data:
            group_id = item.get('id')
            group_name = item['name']
            if group_id:
                group, created = Group.objects.update_or_create(
                    id=group_id,
                    defaults={'name': group_name}
                )
            else:
                group, created = Group.objects.get_or_create(
                    name=group_name
                )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Group '{group_name}' created successfully"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Group '{group_name}' updated successfully"))
