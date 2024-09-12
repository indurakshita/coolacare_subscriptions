import os
import json
from pathlib import Path
from django.core.management.base import BaseCommand
from confapp.models import UILabel

class Command(BaseCommand):
    help = 'Update UILabel model from JSON data'
    
    
    def handle(self, *args, **options):
        base = Path(__file__).resolve().parent.parent
        filepath = base / "json/uilable.json"
        with open(filepath, 'r') as f:
            uilable_json = json.load(f)

        for label_data in uilable_json:
            label_id = label_data.get('id')
            defaults = {
                'page_name': label_data.get('page_name'),
                'type': label_data.get('type'),
                'key': label_data.get('key'),
                'display_value': label_data.get('display_value'),
            }
            try:
                obj, created = UILabel.objects.update_or_create(id=label_id, defaults=defaults)
            except Exception as e:
                self.stderr.write(f'Error updating label {label_id}: {e}')
            else:
                self.stdout.write(f'Successfully {"created" if created else "updated"} label {label_id}')

        self.stdout.write(self.style.SUCCESS('Successfully updated UILabel from JSON data'))


