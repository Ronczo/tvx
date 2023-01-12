from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermissionMetaclass


class IsBudgetSharedPermission(metaclass=BasePermissionMetaclass):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user
        if obj.allowed_to.filter(id=user.id).exists() or obj.user == user:
            return True
        else:
            raise PermissionDenied
