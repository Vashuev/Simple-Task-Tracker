from rest_framework.permissions import BasePermission

class IsUserPermission(BasePermission):
    """
        Permission class for User role only
    """

    def has_permission(self, request, view):
        if request.user.role == 'U' and request.method in ['POST', 'GET']:
            return True
        return False

class IsLeaderOrMemberPermission(BasePermission):
    """
        Permission class for Leader and Member roles
    """
    def has_permission(self, request, view):
        if request.user.role != 'U' and request.method in ['PUT', 'PATCH']:
            return True
        return False
