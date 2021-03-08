from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    
    def has_object_permission(self, request):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_admin