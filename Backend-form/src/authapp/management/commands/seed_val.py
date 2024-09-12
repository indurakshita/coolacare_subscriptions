from django.core.management.base import BaseCommand
import json
from authapp.models.validationmodel import ApiLabel
from pathlib import Path

base = Path(__file__).parent.parent
filepath = base / "json/validation.json"

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open(filepath) as f:
            data = json.load(f)

        for item in data:
            id = item.get('id')
            type = item["type"]
            label = item['label']
            message = item['message']
            action = item['action']
            status_code = item["status_code"]

            if id:
                val, created = ApiLabel.objects.update_or_create(
                    id=id,
                    defaults={'type': type, 'label': label, 'message': message, 'action': action, 'status_code': status_code}
                )
            else:
                val, created = ApiLabel.objects.get_or_create(
                    type=type,
                    label=label,
                    message=message,
                    action=action,
                    status_code=status_code
                )

            if created:
                self.stdout.write(self.style.SUCCESS(f"{type} message created successfully"))
            else:
                self.stdout.write(self.style.SUCCESS(f"{type} message updated successfully"))


