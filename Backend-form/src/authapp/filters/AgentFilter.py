from django.contrib.auth import get_user_model
import django_filters

User = get_user_model()

class AgentFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(lookup_expr='icontains')
    id = django_filters.NumberFilter()
    is_active = django_filters.BooleanFilter(field_name='is_active')
    is_provideradmin = django_filters.BooleanFilter(field_name='is_provideradmin')
    class Meta:
        model = User
        fields = ['email', 'id', 'is_active','is_provideradmin']