from rest_framework import permissions


class IsAdminOrSuperUser(permissions.BasePermission):
    """
    Проверяем является пользователь администратором или суперюзером."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_staff
            or request.user.role == "admin"
        )
