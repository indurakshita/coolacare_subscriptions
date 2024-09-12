from django.urls import path
from subscription.views.subscription_view import SubscriptionAPIView
from subscription.views.payment_view import (
    CreatePaymentIntentView,HandlePaymentConfirmationView,RefundView
)
from subscription.views.slots_views import AvailableSlotsAPIView
from subscription.views.call_schedule_view import SubscriptionScheduleAPIView
from subscription.views.status_views import StatusAPIView
from subscription.views.call_filter_view import ScheduleStatusCombinedView
from subscription.views.schedule_call_combined_view import ScheduleCallCombinedView

from subscription.views.subscription_list_view import subscription_filter
from subscription.views.text_schedule_views import TextAPIView


urlpatterns = [
    path('subscriptions/', SubscriptionAPIView.as_view()), # for get and post
    path('subscriptions/<int:pk>/', SubscriptionAPIView.as_view()) ,# for update and delete 
    path('subscriptions/filter/',subscription_filter.as_view(),name="subscription_filter"),
    path('availableslots/', AvailableSlotsAPIView.as_view(), name="availableslots"),
    path('availableslots/<int:pk>/', AvailableSlotsAPIView.as_view(),name="availableslots"),
    path('schedule/', SubscriptionScheduleAPIView.as_view(), name="schedule"),
    path('schedule/<int:pk>/', SubscriptionScheduleAPIView.as_view(),name="schedule"),
    path('status/', StatusAPIView.as_view(), name="status"),
    path('status/<int:pk>/', StatusAPIView.as_view(),name="status"),

    #for customer page
    path('schedule_status/', ScheduleStatusCombinedView.as_view(),name="schedule_status"),

    #for admin page
    path('schedule/text/', TextAPIView.as_view(), name="schedule_text"),
    path('agent/schedulecall/', ScheduleCallCombinedView.as_view(),name="agent_schedule_view"),
    
    #payments
    path('create_payment_intent/', CreatePaymentIntentView.as_view(), name='create_payment_intent'),
    path("confirm_payment/",HandlePaymentConfirmationView.as_view(),name='confirm_payment_intent'),
    path("refund/",RefundView.as_view(),name="payment_refund")
]
