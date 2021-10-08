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
    class Perm(permissions.BasePermission):
        def has_permission(self, request, view):
            return request.user.has_perm(perm)

    return Perm
