from datetime import datetime
import pytz

def convert_to_24_hours(time_slots):
    converted_slots = []
    for slot in time_slots:
        start_time, end_time = slot.split(" - ")
        start_time_obj = datetime.strptime(start_time, "%I:%M %p")
        end_time_obj = datetime.strptime(end_time, "%I:%M %p")
        converted_slots.append(f"{start_time_obj.strftime('%H:%M')} - {end_time_obj.strftime('%H:%M')}")
    return converted_slots

def convert_to_12_hours(time_slot_utc):
    start_utc_str, end_utc_str = time_slot_utc.split(" - ")
    start_edt = datetime.strptime(start_utc_str, "%H:%M")
    end_edt = datetime.strptime(end_utc_str, "%H:%M")

    return "{} - {}".format(start_edt.strftime("%I:%M %p"), end_edt.strftime("%I:%M %p"))

def convert_time_edt_txt(utc_time_str):
    utc_time = datetime.strptime(utc_time_str, '%H:%M:%S')
    utc_timezone = pytz.utc

    # Combine the time with today's date
    today = datetime.now().date()
    utc_datetime = datetime.combine(today, utc_time.time())

    edt_timezone = pytz.timezone('America/New_York')
    edt_time = utc_timezone.localize(utc_datetime).astimezone(edt_timezone)

    return edt_time.strftime('%I:%M:%S %p')