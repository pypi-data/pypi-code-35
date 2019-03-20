from django.urls import reverse
from django.utils.http import urlquote_plus
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied, ImproperlyConfigured

class TUIDLoginRequiredMixin(object):
    """
    Mixin for class based views which checks, whether the user is logged in
    with TUID and otherwise redirects to login page
    """

    def dispatch(self, request, *args, **kwargs):
        if request.TUIDUser:
            return super().dispatch(request, *args, **kwargs)
        login_url = reverse('pyTUID:login')
        current_url = request.get_full_path()
        return HttpResponseRedirect(login_url + '?next=' + urlquote_plus(current_url))


class TUIDUserInGroupMixin(object):
    """
    Mixin for class based views which checks, whether the logged in TUID user
    is in the given group and raises a PermissionDenied otherwise. If the user
    currently is not logged in with TUID it will be redirected to login page
    """

    group_required = None
    permission_denied_message = None

    def dispatch(self, request, *args, **kwargs):
        if self.group_required is None:
            raise ImproperlyConfigured(
                '{0} is missing the group_required attribute. Define '
                '{0}.group_required.'.format(self.__class__.__name__)
            )
        if request.TUIDUser:
            if request.TUIDUser.in_group(self.group_required):
                return super().dispatch(request, *args, **kwargs)
            if self.permission_denied_message:
                raise PermissionDenied(self.permission_denied_message)
            raise PermissionDenied()
        login_url = reverse('pyTUID:login')
        current_url = request.get_full_path()
        return HttpResponseRedirect(login_url + '?next=' + urlquote_plus(current_url))
