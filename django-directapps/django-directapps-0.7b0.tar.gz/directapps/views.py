#
# Copyright (c) 2016, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
import json
from hashlib import md5

from django.apps import apps as django_apps
from django.db.utils import ConnectionDoesNotExist
from django.http import (HttpResponseBadRequest, HttpResponseForbidden,
                         HttpResponseNotFound, HttpResponseServerError)
from django.core.exceptions import (FieldError, PermissionDenied,
                                    ValidationError as DjangoValidationError)
from django.core.paginator import EmptyPage
from django.urls import reverse
from django.utils.encoding import force_text, force_bytes
from django.utils.module_loading import import_string
from django.utils.translation import ugettext_lazy as _

from directapps import __version__
from directapps.conf import (ACCESS_FUNCTION, EXCLUDE_APPS, EXCLUDE_MODELS,
                             CHECKSUM_VERSION)
from directapps.controllers import get_controller
from directapps.decorators import parse_rest
from directapps.encoders import JSONEncoder
from directapps.exceptions import ValidationError, NotExistError
from directapps.response import make_response
from directapps.utils import get_model_perms, has_model_perms, is_m2m_layer


access = import_string(ACCESS_FUNCTION)


@parse_rest
def director(request, app=None, model=None, model_using=None,
             relation_using=None, **kwargs):
    """
    The main distributor of requests to application models.
    In `kwargs` can be: object, relation, relation_object and action.
    All requirements and error messages are sent strictly in plain text.
    """
    user = request.user

    if not user.is_authenticated:
        return HttpResponseBadRequest(_("You need to login."), status=401)

    if not access(request):
        return HttpResponseForbidden(_("You don't have access to this page."))

    # Return the general scheme of all applications of the "first level".
    # That is, excluding complete model schematics within each application.
    if not app:
        data = get_scheme_apps(request)
        return make_response(data)

    if not user.has_module_perms(app):
        return HttpResponseForbidden(
            _("You don't have access to this application.")
        )

    if app in EXCLUDE_APPS:
        return HttpResponseBadRequest(_('Application is disabled.'))

    try:
        app = django_apps.get_app_config(app)
    except LookupError:
        return HttpResponseNotFound(_('Application not found.'))

    # Return the application scheme including the full schemes of models.
    if not model:
        data = get_scheme_app(request, app, True)
        return make_response(data)

    fullname = '%s.%s' % (app.label, model)
    if model not in app.models:
        return HttpResponseNotFound(_('Model not found.'))
    if fullname in EXCLUDE_MODELS:
        return HttpResponseBadRequest(_('Model is disabled.'))

    model = app.models[model]
    if not has_model_perms(user, model):
        return HttpResponseForbidden(
            _("You don't have access to this model.")
        )

    # Only one use of the database is possible.
    if relation_using:
        kwargs['using'] = relation_using
    elif model_using:
        kwargs['using'] = model_using

    try:
        ctrl = get_controller(model)
        data = ctrl.routing(request, **kwargs)
    except (NotExistError, ConnectionDoesNotExist) as e:
        return HttpResponseNotFound(force_text(e))
    except (FieldError, ValidationError) as e:
        return HttpResponseBadRequest(force_text(e))
    except DjangoValidationError as e:
        return HttpResponseBadRequest('\n'.join(e.messages))
    except PermissionDenied:
        return HttpResponseForbidden(
            _("You don't have access to this action.")
        )
    except (IndexError, model.DoesNotExist, EmptyPage):
        return HttpResponseNotFound(_('Object not found.'))
    except (TypeError, ValueError) as e:
        return HttpResponseBadRequest(force_text(e))
    except NotImplementedError:
        return HttpResponseServerError(_('Not implemented.'))

    return make_response(data)


def version(request):
    data = {
        'checksum': CHECKSUM_VERSION,
        'directapps': __version__,
    }
    return make_response(data)


def get_scheme_model(request, model, full):
    """Returns the full or short scheme of the model."""
    user = request.user
    if not has_model_perms(user, model):
        return

    meta = model._meta
    scheme = {
        'name': meta.model_name,
        'display_name': force_text(meta.verbose_name_plural),
        'url': reverse('directapps:model',
                       args=(meta.app_label, meta.model_name))
    }
    if user.is_superuser:
        scheme['perms'] = 'all'
    else:
        scheme['perms'] = list(get_model_perms(user, model))
    if full:
        scheme.update(get_controller(model).get_scheme(request))
    return scheme


def get_scheme_app(request, app, full):
    """Returns the full or short scheme of the application."""
    user = request.user
    if not user.has_module_perms(app.label):
        return

    models = []
    for model_name, model in app.models.items():
        if is_m2m_layer(model):
            continue
        meta = model._meta
        if meta.swapped or meta.abstract:
            continue
        fullname = '%s.%s' % (app.label, model_name)
        if fullname in EXCLUDE_MODELS:
            continue
        scheme = get_scheme_model(request, model, full=full)
        if scheme:
            models.append(scheme)

    if not models:
        return

    scheme = {
        'name': app.label,
        'display_name': force_text(app.verbose_name),
        'models': models,
        'url': reverse('directapps:app', args=(app.label,)),
        'complete': full,
    }
    return scheme


def get_scheme_apps(request):
    """
    Returns the short scheme as list applications with version and checksum.
    """
    data = []
    for app in django_apps.get_app_configs():
        if app.label in EXCLUDE_APPS:
            continue
        scheme = get_scheme_app(request, app, full=False)
        if scheme:
            data.append(scheme)

    cs = md5(force_bytes(CHECKSUM_VERSION))
    cs.update(force_bytes(__version__))
    dump = json.dumps(data, cls=JSONEncoder, sort_keys=True)
    cs.update(force_bytes(dump))
    scheme = {
        'checksum': cs.hexdigest(),
        'version': __version__,
        'apps': data
    }
    return scheme
