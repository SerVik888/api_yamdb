from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
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
        # url = request.resolver_match.kwargs.get('username')
        return (
            request.user
            and request.user.is_staff
            or not request.user.is_anonymous
            and request.user.role == "admin"
        )

    # def has_object_permission(self, request, view, obj):
    #     if (request.method == 'PATCH'):
    #         return True
    #     return True


# class IsMeRequest(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if (
#             (
#                 request.method == 'POST'
#                 or request.method in permissions.SAFE_METHODS)
#             and request.parser_context.kwargs.get('username') == 'me'
#         ):
#             return True
