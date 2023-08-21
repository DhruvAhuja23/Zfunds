from rest_framework import permissions
from home.utils import RolesEnum


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff