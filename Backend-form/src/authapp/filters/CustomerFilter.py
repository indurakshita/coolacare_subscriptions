import django_filters
from django.contrib.auth import get_user_model

User = get_user_model()
class CustomerFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    id = django_filters.NumberFilter()
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'id', 'is_active']