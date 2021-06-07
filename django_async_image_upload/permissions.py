from rest_framework import permissions


class PresignedUrlViewPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['list','create', 'retrieve']:
            return request.user.is_authenticated or request.user.is_admin
        elif view.action in ['head', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_authenticated:
            return False
        if view.action in ['retrieve', 'create']:
            return obj.user == request.user or request.user.is_admin
        elif view.action in ['update', 'partial_update', 'destroy']:
            return True
        else:
            return False
