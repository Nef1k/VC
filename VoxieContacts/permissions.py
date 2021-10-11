"""
Contain set of custom permissions to use in API Views.

GET, POST, PUT, PATCH and DELETE permissions allow to assign
different permissions per single method in ApiView.

Usage:
    >>> class SomeView(APIView):
    >>>     permission_classes = [GET & IsAuthenticated
    >>>                           | POST & AllowAny]

"""
from rest_framework import permissions


class GET(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'GET'


class POST(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'POST'


class PUT(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'PUT'


class PATCH(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'PATCH'


class DELETE(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'DELETE'


def HasPerm(perm: str):
    """Build permission class that checks if user has given permission."""
    class Perm(permissions.BasePermission):
        def has_permission(self, request, view):
            return request.user.has_perm(perm)

    return Perm
