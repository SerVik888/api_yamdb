from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    Предоставляет полный доступ администратору,
    остальным пользователям даётся доступ только на чтение.
    """

    def has_permission(self, request, view):
        """
        Проверяет, что пользователь является администратором,
        либо метод безопасен.
        """
        return (
            request.method in SAFE_METHODS or (
                request.user.is_authenticated and request.user.is_admin
            )
        )


class AdminModeratorOwnerOrReadOnly(permissions.BasePermission):
    """Предоставляет полуный доступ админу, модератору или автору,
    остальным пользователям даётся доступ только на чтение.
    """

    def has_object_permission(self, request, view, obj):
        """
        Проверяет, что пользователь является администратором,
        модератором, автором контента, либо метод безопасен.
        """
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )
