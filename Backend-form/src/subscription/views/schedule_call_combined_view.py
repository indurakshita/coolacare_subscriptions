from subscription.models.schedule_model_call import SubscriptionScheduleCall
from subscription.models.status_model import ScheduleStatus
from authapp.authentication import JWTAuthenticationBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.db.models import Q
from subscription.models.subscription_model import Subscription
from subscription.serializers.combine_serializers import CombineSubscriptionSerializer, CombineStatusSerializer
from authapp.permissions.group_permission import HasGroupPermission
from subscription.utils.hours_converter import convert_to_12_hours
User = get_user_model()


class ScheduleCallCombinedView(APIView):
    authentication_classes = [JWTAuthenticationBackend]
    model_name = 'SubscriptionScheduleCall'.lower()
    permission_classes = [HasGroupPermission]

    def date_schedule(self, date_from, date_to, **filter_criteria):
        if date_from and date_to:
            filter_criteria['scheduled_date__range'] = [date_from, date_to]
        elif date_from:
            date_to = date_from + timedelta(days=7)
            filter_criteria['scheduled_date__range'] = [date_from, date_to]
        elif date_to:
            date_from = date_to - timedelta(days=7)
            filter_criteria['scheduled_date__range'] = [date_from, date_to]
        else:
            filter_criteria['scheduled_date'] = current_date
        
        return filter_criteria

    def get(self, request):
        try:
            global current_date
            current_date = datetime.today()
            agent = request.query_params.get('agent', None)
            date_from = request.query_params.get("date_from", None)
            date_to = request.query_params.get("date_to", None)
            phone_number = request.query_params.get("phone_number", None)
            status = request.query_params.get("status", None)
            daytime = request.query_params.get('daytime', None)
            time = request.query_params.get('time', None)
            name = request.query_params.get('name', None)
            filter_criteria, combined_data = {}, []

    
            if daytime:
                filter_criteria['avaialbleslote__daytime']=daytime
            if time:
                filter_criteria['avaialbleslote__time']=time
            if phone_number:
                filter_criteria['subscription_id__phone__icontains']=phone_number
            if agent:
                agent_ids = agent.split(",")
                agent_list = User.objects.filter(id__in=agent_ids)
                agent_ids = [user.id for user in agent_list]
                if agent_ids:
                    filter_criteria['agent_user_id__in'] = agent_ids
            if name:
                filter_criteria['subscription_id__first_name__icontains'] = name
                # filter_criteria['subscription_id__last_name__icontains'] = name

            if date_from:
                date_from = datetime.strptime(date_from, "%Y-%m-%d")
            if date_to:
                date_to = datetime.strptime(date_to, "%Y-%m-%d")

            groups = User.objects.filter(id=request.user.id).values_list('groups__name', flat=True)
            if "Agent" in groups or "Admin" in groups:
                filter_criteria = self.date_schedule(date_from, date_to, **filter_criteria)

            else:
                return Response([], status=200)
            
            all_filters = Q(**filter_criteria)
            subscription_schedules =  SubscriptionScheduleCall.objects.filter(all_filters)
            
            for schedule in subscription_schedules:
                agent_user = User.objects.get(id=schedule.agent_user_id).email if schedule.agent_user_id else None
                status_filter = {"callschedule_id":schedule.id}
                if status:
                    status_filter['status'] = status
                schedule_statuses = ScheduleStatus.objects.filter(**status_filter)

                if schedule_statuses:
                    subscription = Subscription.objects.get(id = schedule.subscription_id.id)
                    serializer = CombineSubscriptionSerializer(subscription)
                    serialized_data = {
                        'subscriptionScheduleId': schedule.id,
                        'subscription': serializer.data,
                        'feedback': schedule.feedback,
                        'agent_user_id': agent_user,
                        'scheduled_date': schedule.scheduled_date,
                        'start_time': schedule.start_time,
                        'end_time': schedule.end_time,
                        'day': schedule.avaialbleslote.day,
                        'daytime': schedule.avaialbleslote.daytime,
                        'time': convert_to_12_hours(schedule.avaialbleslote.time),
                        'statuses':CombineStatusSerializer(schedule_statuses, many=True).data,
                    }
                    combined_data.append(serialized_data)
            if combined_data:
                return Response(combined_data)
            else:
                return Response([],status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
