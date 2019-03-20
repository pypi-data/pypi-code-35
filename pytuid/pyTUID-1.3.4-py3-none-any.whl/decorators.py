from functools import wraps

from django.utils.decorators import available_attrs
from django.urls import reverse
from django.utils.http import urlquote_plus
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied


def tuid_user_passes_test(test_func, 
                          raise_exception=False,
                          permission_denied_message=None):
    """
    Decorator that checks wether a user passes the given test, otherwise
    displays the login page or raises a PermissionDenied exception with the
    given message when raise_exception is True.
    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.TUIDUser):
                return view_func(request, *args, **kwargs)
            if raise_exception:
                if permission_denied_message:
                    raise PermissionDenied(permission_denied_message)
                raise PermissionDenied
            login_url = reverse('pyTUID:login')
            current_url = request.get_full_path()
            return HttpResponseRedirect(login_url + '?next=' +
                    urlquote_plus(current_url))
        return _wrapped_view
    return decorator


def tuid_login_required(func=None):
    """
    Decorator for views that checks that the user has logged in with TUID,
    redirects to the log-in page otherwise
    """

    actual_decorator = tuid_user_passes_test(lambda u: u)

    #allow to use tuid_login_required with or without braces
    if func:
        return actual_decorator(func)
    return actual_decorator


def tuid_user_in_group(group, permission_denied_message=None):
    """
    Decorator that checks whether the user is loggedd in and belongs to the
    specified group.
    If the user is not logged in with TUID it will be redirected to login page.
    If the user is not in the group a PermissionDenied exception will be
    raised.
    """

    def group_check(user):
        if user:
            if user.in_group(group):
                return True
            if permission_denied_message:
                raise PermissionDenied(permission_denied_message)
            raise PermissionDenied
        #Otherwise show login page:
        return False

    return tuid_user_passes_test(group_check)

