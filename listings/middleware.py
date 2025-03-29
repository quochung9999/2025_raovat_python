from django.contrib.auth.models import Group
from django.utils.functional import SimpleLazyObject

# Cache the group lookup result to avoid hitting the DB on every request
_moderator_group = None

def get_moderator_group():
    """Gets or creates the moderator group object."""
    global _moderator_group
    if _moderator_group is None:
        try:
            _moderator_group = Group.objects.get(name='Moderators')
        except Group.DoesNotExist:
            # Return None or raise an error, or potentially create it?
            # For now, return None, checks using this should handle None gracefully.
             _moderator_group = None # Explicitly set to None if not found
    return _moderator_group

def check_moderator_status(user):
    """Checks if a user is in the Moderators group."""
    if not user.is_authenticated:
        return False
    moderator_group = get_moderator_group()
    if moderator_group is None:
        return False # Group doesn't exist, so user can't be in it
    # Check group membership efficiently
    # user.groups.filter(pk=moderator_group.pk).exists() might be slightly more efficient
    # but user.groups.filter(name='Moderators').exists() is also clear
    return user.groups.filter(pk=moderator_group.pk).exists()

class RoleMiddleware:
    """
    Middleware to add role check properties (is_moderator) to the request.user object.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Add is_moderator check as a lazy object to avoid unnecessary checks
        # for anonymous users or pages where it's not needed.
        request.user.is_moderator = SimpleLazyObject(lambda: check_moderator_status(request.user))
        response = self.get_response(request)
        return response