from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Permission

class HasGroupPermission(BasePermission):

    def has_permission(self, request, view):
        model_name = getattr(view, 'model_name', None)
        if not model_name:
            raise ValueError("model_name must be set before using the permission class")
        print(model_name)
        user_groups = request.user.groups.all()
        permissions = Permission.objects.filter(group__in=user_groups)

        for permission in permissions:
            if model_name == permission.content_type.model:
                if request.method == 'GET' and permission.codename.startswith('view'):
                    return True
                elif request.method == 'POST' and permission.codename.startswith('add'):
                    return True
                elif request.method in ['PUT', 'PATCH'] and permission.codename.startswith('change'):
                    return True
                elif request.method == 'DELETE' and permission.codename.startswith('delete'):
                    return True

        return False