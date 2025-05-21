from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """Custom permission to only allow admin users."""
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'

class IsInstructorOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow instructors and admins to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.role in ['instructor', 'admin']

class IsClientOrInstructor(permissions.BasePermission):
    """Custom permission to allow clients and instructors."""
    def has_permission(self, request, view):
        return request.user and request.user.role in ['client', 'instructor']

class IsOwnerOrInstructor(permissions.BasePermission):
    """Custom permission to only allow owners of an object or their instructors to edit it."""
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner or their instructor
        return (
            obj == request.user or  # Owner
            (request.user.role == 'instructor' and obj.client_relationships.filter(instructor=request.user).exists())  # Instructor
        )

    def has_permission(self, request, view):
        # This method is not implemented in the original code or the new class
        # It's assumed to exist as it's called in the has_object_permission method
        pass 