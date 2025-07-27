from rest_framework import permissions

class IsAdminOrSelf(permissions.BasePermission):
    """
           Check if the user has permission to access the object.

           Args:
               request: The HTTP request object containing user information.
               view: The view being accessed.
               obj: The object being accessed.

           Returns:
               bool: True if the user is a superuser or the owner of the object, False otherwise.
           """
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj == request.user


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'manager'