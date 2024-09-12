from django.urls import path
from authapp.views import (
    Passwordreset_views as ps,
    activation_views as act,
    auth_views as auth,
    dashboard_views as Dv,  
    provider_admin_view as Pv
)
from authapp.views.auth_views import LoginView,SignupView,UserProfileApi_view
from authapp.views.otp_view import OTPGenerateView,OTPVerifyView
"""
Defines the URL patterns for the authentication application.

The URL patterns include:
- Agent signup view
- Agent view
- Agent set password view
- User activation view
- Password reset request view
- Password reset confirm view
- Agent list view
- Customer list view
- User profile API view
- Login view
- Signup view
"""
urlpatterns = [
    
    path('agent-signup/', auth.AgentSignupView.as_view(), name='signup'),
    path('agent/', auth.AgentView.as_view(), name='agent'),
    path('agent-set-password/', ps.AgentSetPasswordView.as_view(), name='set_password'),
    path('activate/', act.ActivateUserView.as_view(), name='activate_user'),
    path('password/reset/', ps.PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password/reset/confirm/', ps.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('agent-list/', Dv.AgentListView.as_view(), name='agent-list'),
    path('customer-list/',Dv.CustomerListView.as_view(),name='customer-list'),
    path("users_profile/<int:pk>/",UserProfileApi_view.as_view(),name="user_profile"),
    path("users_profile/",UserProfileApi_view.as_view(),name="user_profile"),
    path('login/', LoginView.as_view(), name="login"),
    path('signup/', SignupView.as_view(), name='signupview'),
    path('generate-otp/', OTPGenerateView.as_view(), name='generate-otp'),
    path('verify-otp/', OTPVerifyView.as_view(), name='verify-otp'),
    path("admin_convertion/",Pv.AdminConvertionView.as_view(),name="admin_convertion"),
    path("admin_convertion_verify/",Pv.AdminConvertionVerifyView.as_view(),name="admin_convertion_verify"),

]