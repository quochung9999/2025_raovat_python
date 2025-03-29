from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from functools import wraps

def superuser_required(view_func):
    """
    Decorator for views that checks that the user is a superuser.
    Redirects to login page if not authenticated or raises PermissionDenied if not a superuser.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_superuser:
            raise PermissionDenied("You must be an admin to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

class SuperuserRequiredMixin(UserPassesTestMixin):
    """
    Mixin for class-based views that checks that the user is a superuser.
    """
    def test_func(self):
        return self.request.user.is_superuser