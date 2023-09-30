from rest_framework.permissions import BasePermission


class IsNotAuthenticated(BasePermission):
    """
    Allows access only to those who didn't authenticate.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return True
        else:
            return False
