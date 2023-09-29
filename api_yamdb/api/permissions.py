from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return request.method in SAFE_METHODS
        return request.user.role == 'admin'

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return request.method in SAFE_METHODS
        return request.user.role == 'admin'
