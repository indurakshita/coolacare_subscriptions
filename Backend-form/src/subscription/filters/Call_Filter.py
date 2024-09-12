import django_filters
from subscription.models.schedule_model_call import SubscriptionScheduleCall

class SubscriptionScheduleCallFilter(django_filters.FilterSet):
    start_time=django_filters.TimeFilter(field_name="start_time")
    end_time=django_filters.TimeFilter(field_name="end_time")
    scheduled_date = django_filters.DateFilter(field_name='scheduled_date')
    agent_user_id = django_filters.NumberFilter(field_name='agent_user_id')
    subscription_id = django_filters.NumberFilter(field_name='subscription_id')
    daytime = django_filters.CharFilter(field_name='avaialbleslote__daytime')
    time = django_filters.CharFilter(field_name='avaialbleslote__time')
    day = django_filters.CharFilter(field_name='avaialbleslote__day')
    call_status = django_filters.CharFilter(method='filter_status')

    class Meta:
        model = SubscriptionScheduleCall
        fields = ['start_time','end_time','scheduled_date', 'agent_user_id', 'subscription_id', 'daytime', 'time', 'day', 'call_status']

    def filter_status(self, queryset, name, value):
        return queryset.filter(statuses__status=value)

