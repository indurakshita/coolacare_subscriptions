from subscription.models.subscription_model import Subscription
from subscription.models.payment_model import Payment
from rest_framework.views import APIView
from rest_framework.response import Response
from authapp.authentication import JWTAuthenticationBackend
from authapp.permissions.group_permission import HasGroupPermission

class subscription_filter(APIView):
    authentication_classes = [JWTAuthenticationBackend]
    model_name = 'Subscription'.lower()
    permission_classes = [HasGroupPermission]

    def get(self, request):
        filter_criteria = {}
        filter_fields = ['first_name', 'last_name', 'package', 'status']
        
        for field in filter_fields:
            if request.query_params.get(field):
                filter_criteria[field + '__icontains'] = request.query_params.get(field)

        if request.query_params.get("created_by"):
            filter_criteria.update({"created_by": int(request.query_params.get("created_by"))})

        if request.user.groups.filter(name="Customer").exists():
            filter_criteria["created_by"] = request.user.id

        subscriptions = Subscription.objects.filter(**filter_criteria).order_by("-created_at")
        return Response(subscriptions.values())


    

