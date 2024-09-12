from rest_framework.permissions import BasePermission
from django.conf import settings
from django.contrib.auth.models import Group


def setup_testing_environment(permission):
    if settings.DEBUG:
        return True
    return permission


class AuthenticatedUsers(BasePermission):
    def has_permission(self, request, view):
        return setup_testing_environment(request.user_data is not None)

    def has_object_permission(self, request, view, obj):
        return setup_testing_environment(request.user_data is not None)


class ProviderAdminPermissions(BasePermission):
    def has_permission(self, request, view):
        group = request.user.group.first()

        permissions = group.permissions

        # I want to give permissions based on user permissions



    def has_object_permission(self, request, view, obj):
        True


class Agent(BasePermission):
    def has_permission(self, request, view):
        True

    def has_object_permission(self, request, view, obj):
        True


class User(BasePermission):
    def has_permission(self, request, view):
        True

    def has_object_permission(self, request, view, obj):
        True


class PatientPermissions(BasePermission):
    def has_permission(self, request, view):
        True

    def has_object_permission(self, request, view, obj):
        True
