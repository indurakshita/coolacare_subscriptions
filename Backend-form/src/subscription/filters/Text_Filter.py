import django_filters
from subscription.models.schedule_model_text import SubscriptionScheduleText
from django.utils.dateparse import parse_date
from datetime import timedelta

class ScheduleFilter(django_filters.FilterSet):
    subscription_id = django_filters.CharFilter(field_name='subscription_id__id', lookup_expr='icontains')
    day = django_filters.CharFilter(field_name='day', lookup_expr='icontains')
    time = django_filters.RangeFilter(field_name='time')
    daytime = django_filters.CharFilter(field_name='daytime', lookup_expr='icontains')
    date_from = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    phone_number = django_filters.CharFilter(field_name='subscription_id__phone', lookup_expr='icontains')
    status = django_filters.CharFilter(field_name='status', lookup_expr='icontains')

    class Meta:
        model = SubscriptionScheduleText
        fields = ['subscription_id', 'day', 'time', 'daytime', 'date_from', 'date_to', 'phone_number', 'status']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'date_from' in self.data and 'date_to' not in self.data:
            date_from = parse_date(self.data['date_from'])
            self.data['date_to'] = (date_from + timedelta(days=7)).strftime('%Y-%m-%d')
        elif 'date_to' in self.data and 'date_from' not in self.data:
            date_to = parse_date(self.data['date_to'])
            self.data['date_from'] = (date_to - timedelta(days=7)).strftime('%Y-%m-%d')

    def filter_status(self, queryset, name, value):
        return queryset.filter(text_status__status=value)