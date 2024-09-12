# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from subscription import SubscriptionSchedule
# from datetime import timedelta

# @receiver(post_save, sender=SubscriptionSchedule)
# @receiver(post_save, sender=SubscriptionSchedule)
# def generate_schedule(sender, instance, created, **kwargs):
#     if created:
#         subscription_id = instance.subscription_id
#         scheduled_date = instance.scheduled_date
#         daytime = instance.daytime

#         dayname = ['Monday']  # Only consider Monday for the next 30 days
#         schedule = []
#         for dtime in daytime:
#             current_date = scheduled_date
#             end_date = scheduled_date + timedelta(days=30)
#             while current_date < end_date:
#                 if current_date.strftime('%A') in dayname:
#                     schedule.append({
#                         "subscription_id": subscription_id,
#                         "feedback": "",
#                         "agent_user_id": "",
#                         "scheduled_date": current_date.strftime('%Y-%m-%d'),
#                         "start_time": "",
#                         "end_time": "",
#                         "daytime": dtime
#                     })
#                 current_date += timedelta(days=1)

#         # Process the schedule (e.g., save it to a file or database)
#         print(json.dumps(schedule, indent=4))