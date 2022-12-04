from rest_framework import permissions


class CreateOnly(permissions.BasePermission):
    """
    Object-level permission to allow reading or adding objects.
    """

    def has_permission(self, request, view):
        # Allow HEAD and OPTIONS requests
        if request.method in ['HEAD', 'OPTIONS']:
            return True

        # Allow POST method
        return request.method == 'POST'


    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
