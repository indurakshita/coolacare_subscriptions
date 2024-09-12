from subscription.models.schedule_model_call import SubscriptionScheduleCall
from authapp.authentication import JWTAuthenticationBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.db.models import Q
from subscription.filters.Call_Filter import SubscriptionScheduleCallFilter
from subscription.serializers.combine_serializers import CombineScheduleSerializer
from authapp.permissions.group_permission import HasGroupPermission

User = get_user_model()


class ScheduleStatusCombinedView(APIView):
    authentication_classes = [JWTAuthenticationBackend]
    model_name = 'SubscriptionScheduleCall'.lower()
    permission_classes = [HasGroupPermission]
    serializer_class = CombineScheduleSerializer

    def get_queryset(self):
        user_groups = self.request.user.groups.all()
        user_group_names = [group.name for group in user_groups]
        current_date = datetime.now().date()

        if 'Admin' in user_group_names or 'ProviderAdmin' in user_group_names:
            return SubscriptionScheduleCall.objects.filter(
                scheduled_date__gte=current_date - timedelta(days=30),
                scheduled_date__lte=current_date - timedelta(days=1)
            ).prefetch_related('statuses')
        
        elif 'Customer' in user_group_names:
            return SubscriptionScheduleCall.objects.filter(
                scheduled_date__gte=current_date,
                scheduled_date__lte=current_date + timedelta(days=30)
            ).prefetch_related('statuses')
        return SubscriptionScheduleCall.objects.none()


    def get(self, request):
        filtered_data = SubscriptionScheduleCallFilter(self.request.GET,queryset=self.get_queryset()).qs
        serializer = self.serializer_class(filtered_data, many=True)
        return Response(serializer.data)