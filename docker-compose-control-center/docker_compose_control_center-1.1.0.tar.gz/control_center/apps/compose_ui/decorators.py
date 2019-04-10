from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

# checks permission from function argument (app_label_arg_name)
# i.e. checks user.has_perm(${app_label}.perm_code)
def view_has_perm_from_arg(app_label_arg_name: str, perm_code: str):
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            app_label_arg = kwargs.get(app_label_arg_name)
            user: User = request.user
            if user.has_perm(app_label_arg + "." + perm_code):
                return view(request, *args, **kwargs)
            else:
                return HttpResponseForbidden  # 403 Forbidden is better than 404

        return wrapper

    return decorator
