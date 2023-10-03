from rest_framework import permissions
from rest_framework.exceptions import MethodNotAllowed


class IsUserRequest(permissions.BasePermission):
    """
    Проверяем является пользователь администратором или суперюзером.
    И что он не может отправлять метод 'PUT'"""

    def has_permission(self, request, view):
        if (
            request.method == 'PUT'
                or request.method == 'DELETE'
                and request.parser_context.get('kwargs').get('username') == 'me'
        ):
            raise MethodNotAllowed(request.method)
        elif (
            (
                request.method == 'PATCH'
                or request.method in permissions.SAFE_METHODS
            )
            and request.resolver_match.kwargs.get('username') == 'me'
            and request.user.username
        ):

            return True
        return (
            request.user
            and request.user.is_staff
            or not request.user.is_anonymous
            and request.user.role == "admin"
        )
