from rest_framework import permissions

class IsAuthorOrAdminOrModerator(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object, superusers,
    or moderators to edit or delete it.
    Read permissions are allowed to any request.
    """

    def has_permission(self, request, view):
        """
        Allow read-only access for any request.
        For write actions, check object-level permissions.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        # For write methods (POST, PUT, PATCH, DELETE), object-level permission check will be performed.
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Allow write access only to the author, superusers, or moderators.
        """
        # Read permissions are allowed to any request, so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the author, superusers, or moderators.
        # Check if the user is the author
        if obj.author == request.user:
            return True

        # Check if the user is a superuser
        if request.user.is_superuser:
            return True

        # Check if the user is a moderator (assuming RoleMiddleware adds is_moderator)
        if getattr(request.user, 'is_moderator', False):
            return True

        # Otherwise, deny permission
        return False
