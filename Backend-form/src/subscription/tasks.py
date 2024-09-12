from datetime import datetime, timedelta
from subscription.utils.allocate_slote import check_available_slot_call_platinum,check_available_slot_call_gold
from subscription.models.status_model import ScheduleStatus
from subscription.models.schedule_model_call import SubscriptionScheduleCall
from subscription.models.schedule_model_text import SubscriptionScheduleText
from itertools import product
from icecream import ic

def determine_session_based_on_time(time):
    # Define time ranges for different sessions
    morning_start = datetime.strptime("12:00", "%H:%M").time()
    morning_end = datetime.strptime("15:59", "%H:%M").time()
    afternoon_start = datetime.strptime("16:00", "%H:%M").time()
    afternoon_end = datetime.strptime("19:59", "%H:%M").time()
    evening_start = datetime.strptime("20:00", "%H:%M").time()
    evening_end = datetime.strptime("23:59", "%H:%M").time()

    # Determine the session based on the given time
    if morning_start <= time <= morning_end:
        return "Morning"
    elif afternoon_start <= time <= afternoon_end:
        return "Afternoon"
    elif evening_start <= time <= evening_end:
        return "Evening"
    

from icecream import ic
def book_slot(request,slotes,plan):
    ic(request.package,request.mode_of_call)
    if request.package == "PLATINUM" and request.mode_of_call=="VOICE":
        dayname = slotes.dayname
        session = slotes.session
        time = slotes.time
        current_date = datetime.now().date() + timedelta(days=2)
        end_date = current_date + timedelta(days=plan)
        slots = check_available_slot_call_platinum(days=dayname,sessions=session,times=time)
        if slots:
            black_list = []
            slot_set= set()
            for slot in slots:
                slot_set.add(slot)
            while current_date < end_date:
                if current_date.strftime('%A') in dayname:
                    for slot in slot_set:
                        if slot.available_slots > 0 and slot.day==current_date.strftime('%A'):
                            print(f"{current_date}----{current_date.strftime('%A')}---{slot.daytime}----{slot.time}---Booked")
                            instance_p = SubscriptionScheduleCall.objects.create(
                                subscription_id=request,
                                scheduled_date=current_date,
                                avaialbleslote=slot,
                                feedback=""
                            )

                            ScheduleStatus.objects.create(
                                callschedule_id=instance_p,
                                status='SCHEDULED',
                                timestamp=current_date
                            )                                
                            
                            if slot.id not in black_list:
                                slot.available_slots -= 1 
                                slot.booked_slots += 1
                                black_list.append(slot.id)
                            slot.save()
                    
                current_date += timedelta(days=1)
        
    elif request.package == "GOLD" and request.mode_of_call == "VOICE":
        scheduled_date = datetime.now().date()
        end_date = scheduled_date + timedelta(days=2) + timedelta(days=plan)
        black_list = []
        for current_date in (scheduled_date + timedelta(days=i) for i in range(2, plan + 1)):
            if current_date.strftime('%A') in slotes.dayname:
                slot = check_available_slot_call_gold(days=current_date.strftime('%A'),sessions=slotes.session)
                for slot in slot:
                    if slot.available_slots > 0 and slot.day == current_date.strftime('%A'):
                        print(f"{current_date}----{current_date.strftime('%A')}---{slot.daytime}----{slot.time}---Booked")
                        instance_p = SubscriptionScheduleCall.objects.create(
                            subscription_id=request,
                            scheduled_date=current_date,
                            avaialbleslote=slot,
                            feedback=""
                        )

                        ScheduleStatus.objects.create(
                            callschedule_id=instance_p,
                            status='SCHEDULED',
                            timestamp=current_date
                        )

                        if slot.id not in black_list:
                            slot.available_slots -= 1
                            slot.booked_slots += 1
                            black_list.append(slot.id)
                        slot.save()
    

    elif request.package == "PLATINUM" and request.mode_of_call == "SMS":
        daynames = slotes.dayname
        time_intervals = slotes.time
        time_intervals = [datetime.strptime(time, "%H:%M").time() for time in time_intervals]
        current_date = datetime.now().date() + timedelta(days=2)
        end_date = current_date + timedelta(days=plan)
        
        for day, time in product(daynames, time_intervals):
            current_date = datetime.now().date() + timedelta(days=2)
            while current_date < end_date:
                if current_date.strftime('%A') == day:
                    print(time)
                    session = determine_session_based_on_time(time)
                    print(current_date, day, session,time)
                    instance_g = SubscriptionScheduleText.objects.create(
                        subscription_id=request,
                        schedule_status_id=1,
                        date=current_date,
                        day=day,
                        daytime=session,
                        time=time
                    )

                    ScheduleStatus.objects.create(
                        textschedule_id=instance_g,
                        status='SCHEDULED',
                        timestamp=current_date
                    )
                current_date += timedelta(days=1)
                     



    elif request.package == "GOLD" and request.mode_of_call=="SMS":
        daynames = slotes.dayname
        time_intervals = slotes.time
        time_intervals = [datetime.strptime(time, "%H:%M").time() for time in time_intervals]
        current_date = datetime.now().date() + timedelta(days=2)
        end_date = current_date + timedelta(days=plan)
        
        for day, time in product(daynames, time_intervals):
            current_date = datetime.now().date() + timedelta(days=2)
            while current_date < end_date:
                if current_date.strftime('%A') == day:
                    session = determine_session_based_on_time(time)
                    print(current_date, day, session)
                    instance_g = SubscriptionScheduleText.objects.create(
                        subscription_id=request,
                        schedule_status_id=1,
                        date=current_date,
                        day=day,
                        daytime=session,
                        time=time
                    )

                    ScheduleStatus.objects.create(
                        textschedule_id=instance_g,
                        status='SCHEDULED',
                        timestamp=current_date
                    )
                current_date += timedelta(days=1)
                    
        

    elif request.package == "SILVER" and request.mode_of_call == "SMS":
        daynames = slotes.dayname
        time_intervals = slotes.time
        time_intervals = [datetime.strptime(time, "%H:%M").time() for time in time_intervals]
        current_date = datetime.now().date() + timedelta(days=2)
        end_date = current_date + timedelta(days=plan)

        for day, time in product(daynames, time_intervals):
            current_date = datetime.now().date() + timedelta(days=2)
            while current_date < end_date:
                if current_date.strftime('%A') == day:
                    session = determine_session_based_on_time(time)
                    print(current_date, day, session)
                    instance_g = SubscriptionScheduleText.objects.create(
                        subscription_id=request,
                        schedule_status_id=1,
                        date=current_date,
                        day=day,
                        daytime=session,
                        time=time
                    )

                    ScheduleStatus.objects.create(
                        textschedule_id=instance_g,
                        status='SCHEDULED',
                        timestamp=current_date
                    )
                current_date += timedelta(days=1)
