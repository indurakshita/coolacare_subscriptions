from django.core.management.base import BaseCommand
from confapp.models.conf_model import Configuration
from pathlib import Path
import json

base = Path(__file__).parent.parent
filepath = base / "json/configurations.json"

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open(filepath) as f:
            data = json.load(f)

        for item in data:
            config_id = item.get('id')
            config_type = item['config_type']
            key = item['key']
            value = item['value']
            if config_id:
                config, created = Configuration.objects.update_or_create(
                    id=config_id,
                    defaults={'config_type': config_type, 'key': key, 'value': value}
                )
            else:
                config, created = Configuration.objects.get_or_create(
                    config_type=config_type,
                    key=key,
                    value=value
                )

            if created:
                self.stdout.write(self.style.SUCCESS(f"{config_type} configuration created successfully"))
            else:
                self.stdout.write(self.style.SUCCESS(f"{config_type} configuration updated successfully"))
