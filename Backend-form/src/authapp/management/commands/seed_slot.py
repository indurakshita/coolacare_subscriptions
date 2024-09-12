from django.core.management.base import BaseCommand
from subscription.models.avaialbleslots import AvailableSlots
import json
from pathlib import Path

base = Path(__file__).resolve().parent.parent
filepath = base / "json/slot.json"

class Command(BaseCommand):
    help = 'Update AvailableSlots model from JSON data'


    def handle(self, *args, **options):
        with open(filepath, 'r') as f:
            schedule_json = json.load(f)

        for slot_data in schedule_json:
            slot_id = slot_data.get('id')
            defaults = {
                'day': slot_data.get('day'),
                'daytime': slot_data.get('daytime'),
                'time': slot_data.get('time'),
                'total_slots': slot_data.get('total_slots'),
                'booked_slots': slot_data.get('booked_slots'),
                'available_slots': slot_data.get('available_slots', 0), 
            }
            _, created = AvailableSlots.objects.get_or_create(id=slot_id, defaults=defaults)
            if not created:
                AvailableSlots.objects.filter(id=slot_id).update(**defaults)

        self.stdout.write(self.style.SUCCESS('Successfully updated AvailableSlots from JSON data'))


