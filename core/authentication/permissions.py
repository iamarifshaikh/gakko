# from rest_framework.permissions import BasePermission
# from .models import Administrator

from rest_framework.permissions import BasePermission

class IsAdministrator(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return hasattr(request.user, 'role') and request.user.role == 'Administrator'
        return False