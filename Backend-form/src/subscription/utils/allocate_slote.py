import json
from datetime import timedelta
from subscription.models.avaialbleslots import AvailableSlots
from subscription.models.schedule_model_call import SubscriptionScheduleCall

def check_available_slot_call_platinum(days, sessions=None, times=None):
    available_slots = AvailableSlots.objects.all()
    available_slots = available_slots.filter(day__in=days)
    available_slots = available_slots.filter(daytime__in=sessions)
    available_slots = available_slots.filter(time__in=times)
    if available_slots.exists():
        return available_slots


def check_available_slot_call_gold(days ,sessions=None):
    available_slots = []
    for session in sessions:
        slot = AvailableSlots.objects.filter(day=days, daytime=session, available_slots__gt=0).first()
        if slot:
            available_slots.append(slot)
    return available_slots





    