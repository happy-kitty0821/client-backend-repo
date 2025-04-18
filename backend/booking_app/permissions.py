from rest_framework import permissions

class IsCustomer(permissions.BasePermission):
    """
    Allows access only to authenticated users with the role of 'customer'.
    """

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            getattr(request.user, 'role', '') == 'customer'
        )
