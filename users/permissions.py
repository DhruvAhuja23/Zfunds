from rest_framework import permissions
from home.utils import RolesEnum


class IsAdvisor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == RolesEnum.ADVISOR.value
