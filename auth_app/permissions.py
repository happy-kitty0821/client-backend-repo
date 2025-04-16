from rest_framework import permissions

class IsServiceCenterManager(permissions.BasePermission):
    """
    Custom permission to only allow the assigned manager of a service center to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.center_manager == request.user
    

#this method checks if the given vehicle is owned by the service center in which the manager that tries to edit or delete it  
class IsServiceManagerAndOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and
            request.user.role == 'service_manager'
            and hasattr(request.user, 'servicecenter') 
            and obj.sold_by == request.user.servicecenter
        )
    
#for updating and deleting services of a particular place
class IsServiceManagerAndOwnerForServices(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and
            request.user.role == 'service_manager'
            and hasattr(request.user, 'servicecenter') 
            and obj.provided_by == request.user.servicecenter
        )