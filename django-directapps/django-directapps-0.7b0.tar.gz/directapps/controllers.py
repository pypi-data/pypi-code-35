#
# Copyright (c) 2016, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
import logging
import weakref

from django.contrib.auth.hashers import mask_hash, identify_hasher
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import (
    Q, Model, Manager,
    CharField, DateTimeField, DateField, ManyToManyField,
)
from django.db.models.fields import AutoField
from django.db.models.fields.files import FieldFile
from django.forms.models import modelform_factory
from django.urls import reverse
from django.utils.dateparse import parse_datetime, parse_date
from django.utils.encoding import force_text
from django.utils.module_loading import import_string
from django.utils.six import string_types
from django.utils.translation import ugettext_lazy as _

from directapps import conf
from directapps.exceptions import ValidationError, NotExistError
from directapps.shortcuts import smart_search
from directapps.utils import serialize_field, join_display_names_lazy

UNUSABLE_PASSWORD_PREFIX = '!'
MASK_PASSWORD_FIELDS = conf.MASK_PASSWORD_FIELDS

logger = logging.getLogger(__name__)


class BaseController(object):
    """
    A base class of controllers that work directly with models, managers,
    and model fields.

    Includes some of the implemented activities:

    1. `scheme` - returns the scheme of the controller;
    2. `defaults` - returns the default values for the fields in the model
       objects.
    3. `create` - creates one model object (synonym: `action_post`).
    4. `update` - updates one or more model objects
       (synonyms: `action_put` and `action_patch`).
    5. `delete` - deletes one or more model objects.

    """
    # Valid request methods for the actions.
    valid_actions = conf.VALID_ACTIONS
    # A list of fields that should be skipped during the building of the
    # controllers.
    exclude_fields = ()
    # Specifies the related objects that you want to retrieve completely
    # for the query. If it is necessary to forbid it, then to put False.
    select_related = None
    # Defines a list of m2m fields to be retrieved at a time, in addition to
    # the query. If it is necessary to forbid it, then put False.
    prefetch_related = None
    # Dictionary of filters that are always added to the QuerySet in the
    # method get_queryset().
    queryset_filters = None
    # The key by which data is received for search.
    search_key = conf.SEARCH_KEY
    # The key by which the name of the field or column with a relation
    # (for the "_fkey" action) is received from the client.
    foreign_key = conf.FOREIGN_KEY
    # Annotations to the object property or method which is called without
    # any parameters.
    annotations = None

    def __init__(self, model_or_manager, **kwargs):
        """Initialization using the model Manager."""
        if isinstance(model_or_manager, Manager):
            self.manager = model_or_manager
            self.model = self.manager.model
        else:
            self.model = model_or_manager
            self.manager = self.model._default_manager

        meta = self.model._meta
        app_label = meta.app_label
        model_name = meta.model_name
        self.model_full_name = app_label + '.' + model_name
        view_perm = '%s.view_%s' % (app_label, model_name)
        if 'view' in meta.default_permissions or view_perm in meta.permissions:
            self.view_perm = view_perm
        else:
            self.view_perm = None
        self.add_perm = '%s.add_%s' % (app_label, model_name)
        self.change_perm = '%s.change_%s' % (app_label, model_name)
        self.delete_perm = '%s.delete_%s' % (app_label, model_name)

        all = [f for f in meta.fields if f.name not in self.exclude_fields]
        if meta.many_to_many:
            all.extend([f for f in meta.many_to_many if
                        f.name not in self.exclude_fields])

        self.all_fields = all
        self.all_fields_names = [f.name for f in all]

        self.visible_fields = [f for f in all if not f.hidden]
        self.default_fields = [f for f in all if f.has_default()]
        self.editable_fields = [
            f for f in self.visible_fields
            if f.editable and not isinstance(f, AutoField) and
            f.name != 'password'
        ]
        self.editable_fields_names = [f.name for f in self.editable_fields]

        if self.select_related is None:
            self.select_related = [f.name for f in meta.fields if
                                   f.name not in self.exclude_fields and
                                   f.related_model]
        if self.prefetch_related is None:
            self.prefetch_related = [f.name for f in meta.many_to_many if
                                     f.name not in self.exclude_fields]

        if self.annotations is None:
            self.annotations = ()

    def __str__(self):
        return '<%s for %s>' % (self.__class__.__name__, self.model_full_name)

    def get_queryset(self, request, using=None, **kwargs):
        qs = self.manager.all()
        if using:
            qs = qs.using(using)
        if self.queryset_filters:
            qs = qs.filter(**self.queryset_filters)
        return qs

    def render_field(self, request, obj, field):
        """Renders the field of the model object."""
        if '.' in field:
            data = obj
            for part in field.split('.'):
                if data is None:
                    break
                data = getattr(data, part, None)
            field = part
        else:
            data = getattr(obj, field, None)
        if MASK_PASSWORD_FIELDS and field == 'password' and data:
            if data.startswith(UNUSABLE_PASSWORD_PREFIX):
                return None
            try:
                hasher = identify_hasher(data)
            except ValueError:
                return {_('hash'): mask_hash(data)}
            return hasher.safe_summary(data)
        if isinstance(data, FieldFile):
            if data.name:
                return data.url
            return None
        elif isinstance(data, Model):
            return [data.pk, force_text(data)]
        elif isinstance(data, Manager):
            return [(i.pk, force_text(i)) for i in data.all()]
        return data

    def render_annotate(self, request, obj, annotate):
        """
        Renders an annotation, property, or method called without parameters.
        """
        data = getattr(obj, annotate, None)
        if callable(data):
            data = data()
        return data

    def render_objects(self, request, qs):
        """Renders the whole received a QuerySet."""
        render = self.render_field
        render_annotate = self.render_annotate
        fields = self.all_fields_names
        annotations = self.annotations
        meta = self.model._meta
        app_label = meta.app_label
        model_name = meta.model_name

        def serialize(o):
            reverse_args = (app_label, model_name, o.pk)
            return {
                'fields': {f: render(request, o, f) for f in fields},
                'annotations': {a: render_annotate(request, o, a) for a in
                                annotations},
                'pk': o.pk,
                'display_name': force_text(o),
                'url': reverse('directapps:object', args=reverse_args)
            }

        return [serialize(o) for o in qs]

    def get_list_id(self, request, object=None, relation_object=None,
                    rasing=True, **kwargs):
        """Returns a list of identifiers from the query."""
        if object:
            list_id = [object]
        elif relation_object:
            list_id = [relation_object]
        else:
            list_id = request.data.get('id')
            if not list_id:
                if rasing:
                    raise ValidationError(
                        _('The request body does not contain the list id.')
                    )
                else:
                    return None
            if isinstance(list_id, string_types):
                if list_id.startswith('[') and list_id.endswith(']'):
                    list_id = list_id[1:-1]
                list_id = list_id.split(',')
        return list_id

    def get_model_form(self, request, fields=None, **kwargs):
        if not fields:
            fields = self.editable_fields_names
        else:
            fields = [f for f in self.editable_fields_names if f in fields]
        if not fields:
            raise ValidationError(_('Not contains fields for object.'))
        kw = {}
        if hasattr(self, 'form'):
            kw['form'] = self.form
        return modelform_factory(self.model, fields=fields, **kw)

    def prepare_request_data(self, data):
        """
        Function pre-processes the data to form models.

        This is necessary to convert dates and times to ISO format, as well as
        to ManyToManyField.

        Skips all nonexistent model fields as well as those that are not
        editable.

        Here `data` - it's django.http.request.QueryDict or dictionary.
        """
        params = {}
        get_field = self.model._meta.get_field
        editable_fields = self.editable_fields
        for k in data.keys():
            try:
                field = get_field(k)
            except:
                continue
            if field not in editable_fields:
                continue
            if isinstance(field, ManyToManyField):
                method = getattr(data, 'getlist', data.get)
                v = method(k)
                if not isinstance(v, (list, tuple)):
                    v = [v]
                try:
                    params[k] = [x for x in (v or []) if x]
                except:
                    params[k] = v
                continue
            v = data[k]
            if isinstance(field, DateTimeField):
                try:
                    params[k] = parse_datetime(v)
                except:
                    params[k] = v
            elif isinstance(field, DateField):
                try:
                    params[k] = parse_date(v)
                except:
                    params[k] = v
            else:
                params[k] = v
        return params

    def get_scheme(self, request, **kwargs):
        return 'NotImplemented'

    def validate(self, request, action):
        if action != action.lower():
            raise ValidationError(_('The action name must be in lower case.'))
        valid = self.valid_actions
        method = request.method
        if action in valid and method not in valid[action]:
            raise ValidationError(
                _("Method '%s' is forbidden for action.") % method
            )
        return True

    def routing(self, request, action=None, **kwargs):
        """Provides routing to methods."""
        if action:
            pass
        elif request.method == 'POST' and '_method' in request.data:
            action = request.data['_method'].lower()
        else:
            action = request.method.lower()
        self.validate(request, action)
        handler = getattr(self, 'action_%s' % action, None)
        if not handler:
            raise NotExistError(_("Action '%s' not exist.") % action)
        return handler(request, **kwargs)

    # Getting #

    def action_get(self, request, **kwargs):
        raise NotImplementedError()

    # Creating #

    def action_create(self, request, **kwargs):
        user = request.user
        if not user.has_perm(self.add_perm):
            raise PermissionDenied()

        model_form = self.get_model_form(request)
        files = request.FILES
        data = self.prepare_request_data(request.data)
        fields = list(data.keys()) + list(files.keys())
        model_form = self.get_model_form(request, fields)
        form = model_form(data, files=files)
        if form.is_valid():
            try:
                o = form.save(commit=False)
                o.save(using=kwargs.get('using'))
            except Exception as e:
                logger.error(e)
                raise e
            else:
                logger.info(
                    'User #%s has created an object <%s#%s> "%s"',
                    user.pk, self.model_full_name, o.pk, o
                )
        else:
            logger.error(form.errors.as_text())
            raise ValidationError(form.errors.as_json())
        return self.render_objects(request, [o])[0]

    def action_post(self, *args, **kwargs):
        return self.action_create(*args, **kwargs)

    def action_add(self, *args, **kwargs):
        return self.action_create(*args, **kwargs)

    # Updating #

    def action_update(self, request, **kwargs):
        user = request.user
        if not user.has_perm(self.change_perm):
            raise PermissionDenied()

        list_id = self.get_list_id(request, **kwargs)
        files = request.FILES
        data = self.prepare_request_data(request.data)
        fields = list(data.keys()) + list(files.keys())
        model_form = self.get_model_form(request, fields)

        qs = self.get_queryset(request, **kwargs)
        qs = qs.filter(pk__in=list_id)
        result = []
        for o in qs:
            form = model_form(data, files=files, instance=o)
            if form.is_valid():
                try:
                    o = form.save(commit=False)
                    o.save(using=kwargs.get('using'))
                    result.append(o)
                except Exception as e:
                    logger.error(e)
                    raise e
                else:
                    logger.info(
                        'User #%s has updated an object <%s#%s> "%s"',
                        user.pk, self.model_full_name, o.pk, o
                    )
            else:
                logger.error(form.errors.as_text())
                raise ValidationError(form.errors.as_json())
        # If one object was specified for update, we will return one.
        data = self.render_objects(request, result)
        if len(list_id) == 1:
            return data[0] if data else None
        return data

    def action_put(self, *args, **kwargs):
        return self.action_update(*args, **kwargs)

    def action_patch(self, *args, **kwargs):
        return self.action_update(*args, **kwargs)

    # Deleting #

    def action_delete(self, request, **kwargs):
        user = request.user
        if not user.has_perm(self.delete_perm):
            raise PermissionDenied()

        list_id = self.get_list_id(request, **kwargs)
        qs = self.get_queryset(request, **kwargs)
        qs = qs.filter(pk__in=list_id)
        result = []
        for o in qs:
            try:
                pk = o.pk
                display_name = force_text(o)
                o.delete(using=kwargs.get('using'))
            except Exception as e:
                logger.error(e)
                pass
            else:
                logger.info(
                    'User #%s has deleted an object <%s#%s> "%s"',
                    user.pk, self.model_full_name, pk, display_name
                )
                result.append(pk)
        return result

    # Default values #

    def action_defaults(self, request, **kwargs):
        """
        Returns the default values for the fields in which they are defined.
        """
        return {f.name: f.get_default() for f in self.default_fields}

    # Scheme #

    def action_scheme(self, request, **kwargs):
        """Returns the scheme of the controller."""
        return self.get_scheme(request, **kwargs)

    # The search for external models #

    def action_fkey(self, request, **kwargs):
        """Returns data for the relationship model."""
        user = request.user
        if self.view_perm and not user.has_perm(self.view_perm):
            raise PermissionDenied()
        data = {k: request.GET[k] for k in request.GET.keys()}
        query = data.get(self.search_key, None)
        fname = data.get(self.foreign_key, None)
        # Column mapping is performed only for the model.
        if hasattr(self, 'map_column_field'):
            if fname in self.map_column_field:
                fname = self.map_column_field[fname]
        try:
            assert fname is not None
            names = fname.split('__')
            model = self.model
            for name in names:
                field = model._meta.get_field(name)
                limit_choices_to = field.get_limit_choices_to()
                model = field.remote_field.model
        except:
            raise ValidationError(_('Please send correct relation name.'))
        ctrl = get_controller(field.remote_field.model).model_ctrl
        qs = ctrl.get_queryset(request, **kwargs)
        if limit_choices_to:
            qs = qs.filter(**limit_choices_to)
        return ctrl.simple_search(request, query, qs, **kwargs)


class ModelController(BaseController):
    """Контроллер операций с коллекцией объектов (моделью)."""
    # The filter list is automatically populated with all its own fields and
    # all relationship fields, unless an empty list is specified.
    filters = None
    # The list of columns consists of dictionaries formed with the function
    # serialize_field().
    columns = None
    # List of column names by which to sort.
    order_columns = None
    # List of fields for general search (see `search_key`).
    search_fields = None
    # Associate columns with real fields.
    map_column_field = None
    # Associate columns with other models on the client.
    map_column_relation = None
    # The key by which the list of fields for rendering is received.
    columns_key = conf.COLUMNS_KEY
    # The key by which sorting is accepted from the client.
    ordering_key = conf.ORDERING_KEY
    # The key by which the limit of records is accepted from the client.
    limit_key = conf.LIMIT_KEY
    # The key by which the client receives the page number.
    page_key = conf.PAGE_KEY
    # Working limit of returned records.
    limit = conf.LIMIT
    # The maximum limit of returned records, which does not allow to kill the
    # server with huge data sets.
    max_limit = conf.MAX_LIMIT

    def __init__(self, *args, **kwargs):
        """Initialization."""

        BaseController.__init__(self, *args, **kwargs)

        self.default_ordering = self.model._meta.ordering

        if self.map_column_field is None:
            self.map_column_field = {}
        if self.map_column_relation is None:
            self.map_column_relation = {}

        self.autoset_filters()
        self.autoset_columns()

        if self.order_columns is None:
            self.order_columns = [f.name for f in self.visible_fields if
                                  not f.related_model]
        if self.search_fields is None:
            fields = [f.name for f in self.visible_fields if
                      isinstance(f, CharField) and f.name != 'password']
            if not fields:
                for field in self.visible_fields:
                    rel = field.related_model
                    if rel:
                        prefix = field.name + '__%s'
                        fields.extend([
                            prefix % f.name for f in rel._meta.fields if
                            not f.hidden and isinstance(f, CharField) and
                            f.name != 'password'
                        ])
            self.search_fields = fields

    def autoset_filters(self):
        def serialize(f, parent=None):
            data = {'type': f.__class__.__name__}
            if parent:
                data['name'] = '%s__%s' % (parent.name, f.name)
                data['display_name'] = join_display_names_lazy(
                    parent.verbose_name, f.verbose_name
                )
            else:
                data['name'] = f.name
                data['display_name'] = f.verbose_name
            if f.choices:
                data['choices'] = f.get_choices(include_blank=False)
            return data

        if self.filters is None:
            L = []
            for field in self.all_fields:
                if field.name == 'password':
                    continue
                L.append(serialize(field))
                rel = field.related_model
                if rel:
                    L.extend([
                        serialize(f, field) for f in rel._meta.fields if
                        f.name != 'password'
                    ])
            self.filters = L

        L = [f['name'] for f in self.filters]
        L.sort()
        L.reverse()
        self.names_filters = L

    def autoset_columns(self):
        def test(f):
            return bool(
                hasattr(f, 'auto_now_add') or
                hasattr(f, 'auto_now') or not
                (f.hidden or f.name == 'password')
            )

        if self.columns is None:
            self.columns = [serialize_field(f) for f in self.all_fields if
                            test(f)]

    def get_scheme(self, request, **kwargs):
        """
        Returns a model schema that can be used to display model objects on
        the client.
        """
        data = {
            'filters': self.filters,
            'columns': self.columns,
            'default_ordering': self.default_ordering,
            'order_columns': self.order_columns,
            'map_column_relation': self.map_column_relation,
            'columns_key': self.columns_key,
            'ordering_key': self.ordering_key,
            'search_key': self.search_key if self.search_fields else None,
            'limit_key': self.limit_key,
            'page_key': self.page_key,
            'foreign_key': self.foreign_key,
            'limit': self.limit,
            'max_limit': self.max_limit,
        }
        return data

    def render_column(self, request, obj, column):
        """Renders a column for a record."""
        if column in ('__unicode__', '__str__'):
            return force_text(obj)
        column = column.replace('__', '.')
        display = 'get_%s_display' % column
        if hasattr(obj, display):
            # It's a choice field
            return [getattr(obj, column), getattr(obj, display)()]
        else:
            return self.render_field(request, obj, column)

    def render_objects(self, request, qs, columns=None):
        """Renders the whole received a QuerySet."""
        render = self.render_column
        render_annotate = self.render_annotate
        M = self.map_column_field
        fields = [M.get(col['name'], col['name']) for col in self.columns if
                  columns is None or col['name'] in columns]
        annotations = self.annotations
        meta = self.model._meta
        app_label = meta.app_label
        model_name = meta.model_name

        def serialize(o):
            reverse_args = (app_label, model_name, o.pk)
            return {
                'fields': {f: render(request, o, f) for f in fields},
                'annotations': {a: render_annotate(request, o, a) for a in
                                annotations},
                'pk': o.pk,
                'display_name': force_text(o),
                'url': reverse('directapps:object', args=reverse_args)
            }

        return [serialize(o) for o in qs]

    def filtering(self, request, qs, filters):
        """Filters the dataset."""
        if not filters:
            return qs

        def test_filtered(field):
            for f in self.names_filters:
                if field.startswith(f):
                    return True
            return False

        def test_inverse(s):
            return s.startswith('-')

        def test_bool(s, v):
            return s.endswith('__isnull') or v in ('true', 'false')

        def test_list(s):
            return s.endswith('__in') or s.endswith('__range')

        for field, query in filters.items():
            if field == self.search_key:
                qs = smart_search(qs, self.search_fields, query)
                continue

            if test_inverse(field):
                field = field[1:]
                func = qs.exclude
            else:
                func = qs.filter

            if not test_filtered(field):
                continue

            if isinstance(query, string_types):
                if query.startswith('[') and query.endswith(']'):
                    query = [x for x in query[1:-1].split(',') if x]
                elif test_list(field):
                    query = [x for x in query.split(',') if x]
                elif test_bool(field, query):
                    query = bool(query == 'true')

            qs = func(Q(**{field: query}))
        return qs

    def ordering(self, request, qs, ordering):
        """
        The function checks the collation and applies only the valid.
        """
        if not ordering or not self.order_columns:
            # Fix UnorderedObjectListWarning:
            if not getattr(qs, 'ordered', True):
                qs = qs.order_by('pk')
            return qs

        def valid(x):
            return bool(
                x and not x.startswith('--') and
                x.lstrip('-') in self.order_columns
            )

        if isinstance(ordering, string_types):
            if ordering.startswith('[') and ordering.endswith(']'):
                ordering = ordering[1:-1]
            ordering = ordering.split(',')
        ordering = [x for x in ordering if valid(x)]
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def paging(self, request, qs, page, limit, orphans=0):
        """The function returns the Page object of Paginator."""
        return Paginator(qs, per_page=limit, orphans=orphans).page(page)

    def info(self, request, qs):
        """
        Returns information about the set. Can be freely to change under
        inheritance.
        """
        return None

    def context(self, request, page, info, columns):
        """The formation of the context of the JSON structure."""
        data = {
            'objects': self.render_objects(request, page.object_list, columns),
            'page': page.number,
            'num_pages': page.paginator.num_pages,
            'info': info,
        }
        return data

    def action_get(self, request, **kwargs):
        """Standard getting the data."""
        user = request.user
        if self.view_perm and not user.has_perm(self.view_perm):
            raise PermissionDenied()
        data = {k: request.GET[k] for k in request.GET.keys()}
        page = data.pop(self.page_key, None)
        page = int(page or 1)
        limit = data.pop(self.limit_key, None)
        limit = int(limit or self.limit)
        if limit > self.max_limit:
            limit = self.max_limit
        ordering = data.pop(self.ordering_key, None)
        columns = data.pop(self.columns_key, None)
        if columns is not None:
            columns = columns.split(',')
        filters = data
        # Get the entire QuerySet together with the dependent objects.
        # Named parameters are required for inheritance, do not remove them!
        qs = self.get_queryset(request, **kwargs)
        if isinstance(self.select_related, (list, tuple)):
            qs = qs.select_related(*self.select_related)
        elif self.select_related:
            qs = qs.select_related()
        if isinstance(self.prefetch_related, (list, tuple)):
            qs = qs.prefetch_related(*self.prefetch_related)
        elif self.prefetch_related:
            qs = qs.prefetch_related()
        # Filter, sort and render the result.
        qs = self.filtering(request, qs, filters)
        info = self.info(request, qs)
        qs = self.ordering(request, qs, ordering)
        page = self.paging(request, qs, page, limit)
        ctx = self.context(request, page, info, columns)
        return ctx

    def simple_search(self, request, query, qs=None, **kwargs):
        """Simple search for model objects."""
        user = request.user
        if self.view_perm and not user.has_perm(self.view_perm):
            raise PermissionDenied()
        if qs is None:
            qs = self.get_queryset(request, **kwargs)
        if query:
            if not self.search_fields:
                qs = qs.filter(pk=query)
            else:
                qs = self.filtering(request, qs, {self.search_key: query})

        def serialize(o):
            return {
                'pk': o.pk,
                'display_name': force_text(o),
            }

        return [serialize(o) for o in qs[:10]]


class RelationController(ModelController):
    """Controller of operations with related models."""

    def __init__(self, rel):
        """Initialization."""

        self.rel = rel
        self.field_name = rel.field.name
        ModelController.__init__(self, rel.related_model)
        self.relation_name = force_text(self.model._meta)

    def autoset_columns(self):
        if self.columns is None:
            self.columns = [serialize_field(f) for f in self.visible_fields if
                            f.name != self.field_name]

    def get_queryset(self, request, object, **kwargs):
        qs = ModelController.get_queryset(self, request, **kwargs)
        qs = qs.filter(**{'%s__exact' % self.field_name: object})
        return qs

    def get_scheme(self, request, **kwargs):
        data = ModelController.get_scheme(self, request, **kwargs)
        data['relation'] = self.relation_name
        return data


class ObjectController(BaseController):
    """Controller of operations with the object."""

    # The next 2 parameters are defined together.
    # List of related models with their names [('order', 'Заказы'),].
    relations = None
    # Map of related models and their controllers.
    map_relation_ctrl = None

    def __init__(self, *args, **kwargs):
        """Initialization."""

        BaseController.__init__(self, *args, **kwargs)

        meta = self.model._meta
        self.serialized_fields = [serialize_field(f) for f in
                                  self.visible_fields]

        if self.map_relation_ctrl is None:
            self.map_relation_ctrl = {}

        if self.relations is None:
            R = []
            for rel in meta.related_objects:
                ctrl = RelationController(rel)
                self.map_relation_ctrl[rel.name] = ctrl
                R.append([rel.name,
                          rel.related_model._meta.verbose_name_plural])
            self.relations = R

    def get_scheme(self, request, **kwargs):
        """
        Returns a model schema that can be used to create or update model
        objects on the client.
        """
        data = {
            'fields': self.serialized_fields,
            'relations': [
                {
                    'name': r[0],
                    'display_name': r[1],
                    'relation': self.map_relation_ctrl[r[0]].relation_name
                } for r in self.relations
            ],
            'foreign_key': self.foreign_key,
            'search_key': self.search_key,
            'display_name': self.model._meta.verbose_name,
        }
        return data

    def routing(self, request, relation=None, **kwargs):
        """Provides routing to methods (relationships or self)."""
        if relation:
            try:
                ctrl = self.map_relation_ctrl[relation]
            except KeyError:
                raise NotExistError(_("Relation '%s' not exist.") % relation)
            return ctrl.routing(request, **kwargs)
        return BaseController.routing(self, request, **kwargs)

    def action_get(self, request, object, **kwargs):
        """Returns a model object."""
        user = request.user
        if self.view_perm and not user.has_perm(self.view_perm):
            raise PermissionDenied()
        qs = self.get_queryset(request, **kwargs)
        obj = qs.get(pk=object)
        return self.render_objects(request, [obj])[0]


class MasterController(object):
    """
    Master controller that combines other controllers and performs routing
    to them.
    """

    model_ctrl = None
    model_ctrl_class = ModelController
    object_ctrl = None
    object_ctrl_class = ObjectController

    def contribute_to_class(self, model, name):
        """
        The method is called when the master controller is added to the model
        via model.add_to_class(), or at the time of initialization of the
        model in which the controller is defined by an attribute.
        """
        # We are used a `weakref` because of possible memory leaks
        # (circular reference).
        self.model = weakref.ref(model)()
        self.name = name
        setattr(model, name, self)
        # Creating an attribute, by which will be available the
        # master-controller.
        if not getattr(model, conf.ATTRIBUTE_NAME, None):
            setattr(model, conf.ATTRIBUTE_NAME, weakref.ref(self)())
        # Install all necessary sub-controllers.
        self.install_ctrls()

    def install_ctrls(self):
        """Sets the instances of all the necessary controllers."""
        self.model_ctrl = self.model_ctrl_class(self.model)
        self.object_ctrl = self.object_ctrl_class(self.model)

    def routing(self, request, **kwargs):
        """Provides routing to sub-controllers."""
        if 'object' in kwargs:
            return self.object_ctrl.routing(request, **kwargs)
        return self.model_ctrl.routing(request, **kwargs)

    def get_scheme(self, request, **kwargs):
        """Returns the full scheme of the model."""
        scheme = self.model_ctrl.get_scheme(request)
        scheme['object'] = self.object_ctrl.get_scheme(request)
        return scheme


def get_controller(model):
    """Returns an instance of the controller associated with the model."""
    name = conf.ATTRIBUTE_NAME
    if not hasattr(model, name):
        # set controller to model
        m = model._meta
        ctrl = conf.CONTROLLERS.get('%s.%s' % (m.app_label, m.model_name))
        if ctrl:
            ctrl = import_string(ctrl)()
        elif conf.MASTER_CONTROLLER:
            ctrl = import_string(conf.MASTER_CONTROLLER)()
        else:
            ctrl = MasterController()
        model.add_to_class(name, ctrl)
    elif not isinstance(getattr(model, name), MasterController):
        ctrl = getattr(model, name)()
        model.add_to_class(name, ctrl)
    return getattr(model, name)
