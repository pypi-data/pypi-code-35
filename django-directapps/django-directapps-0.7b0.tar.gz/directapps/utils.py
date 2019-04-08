#
# Copyright (c) 2016, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
from django.utils.encoding import force_text
from django.utils.functional import lazy

from directapps.conf import MASK_PASSWORD_FIELDS


def get_all_model_perms(model):
    """Returns an iterator of all model permissions."""
    meta = model._meta
    app_label = meta.app_label
    model_name = meta.model_name
    for p in meta.permissions:
        yield '%s.%s' % (app_label, p[0])
    for p in meta.default_permissions:
        yield '%s.%s_%s' % (app_label, p, model_name)


def get_model_perms(user, model):
    """Returns an iterator of all permissions available to the user."""
    for p in get_all_model_perms(model):
        if user.has_perm(p):
            yield p


def has_model_perms(user, model):
    """Checks whether the model is available to the user."""
    for p in get_model_perms(user, model):
        return True
    return False


def is_m2m_layer(model):
    """
    Checks whether the model is a binding for the field `ManyToManyField`.
    """
    meta = model._meta
    fields = meta.fields
    if len(fields) == 3:
        f0, f1, f2 = fields
        if f1.remote_field and f2.remote_field:
            if f1.remote_field.one_to_many and f2.remote_field.one_to_many:
                return True
    return False


def serialize_field(f):
    """Serializes model fields."""
    data = {
        'name': f.name,
        'type': f.__class__.__name__,  # like get_internal_type()
        'display_name': f.verbose_name,
    }
    if f.name == 'password':
        data['mask_password'] = MASK_PASSWORD_FIELDS
    if f.max_length:
        data['max_length'] = f.max_length
    if f.description:
        data['description'] = f.description % data
    if f.help_text:
        data['help_text'] = f.help_text
    if f.choices:
        data['choices'] = f.get_choices(include_blank=False)
    if f.related_model:
        m = f.related_model._meta
        data['relation'] = '%s.%s' % (m.app_label, m.model_name)

    if f.has_default():
        data['has_default'] = True
        is_callable = callable(f.default)
        # Because fields can and should be serialized long before objects are
        # created, the client application must calculate the value. Therefore,
        # the client must understand and convert the "auto" value in real time.
        is_auto = data['type'] in (
            'DateField', 'DateTimeField', 'TimeField', 'UUIDField',
        )
        if is_auto and is_callable:
            data['default'] = 'auto'
        elif is_callable:
            data['default'] = f.default()
        else:
            data['default'] = f.default
    # True boolean fields send only
    if f.primary_key:
        data['primary_key'] = True
    if f.unique:
        data['unique'] = True
    if not f.editable or f.auto_created:
        data['readonly'] = True
    if f.null:
        data['null'] = True
    if f.blank:
        data['blank'] = True
    if f.hidden:
        data['hidden'] = True
    if f.many_to_many:
        data['many_to_many'] = True
    if f.many_to_one:
        data['many_to_one'] = True
    if f.one_to_many:
        data['one_to_many'] = True
    if f.one_to_one:
        data['one_to_one'] = True

    return data


def join_display_names(*args):
    return ': '.join([force_text(s) for s in args])


join_display_names_lazy = lazy(join_display_names, str)
