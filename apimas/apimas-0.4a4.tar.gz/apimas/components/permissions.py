import specular
from apimas.base import ProcessorFactory
from apimas import documents as doc
from apimas import utils
from apimas.errors import AccessDeniedError, InvalidInput
from apimas.tabmatch import Tabmatch


Leaf = object()


FIELD_SEPARATOR = '/'


_default_rules = []



def add_prefixed(namespace, data, prefix):
    for key, value in data.iteritems():
        namespace[prefix + key] = value


def _is_prefixed(path, prefix=None):
    if prefix is None:
        return False
    prefix_len = len(prefix)
    return prefix_len < len(path) and path[:prefix_len] == prefix


def expand_paths(matched_fields, fields_spec):
    if matched_fields is doc.ANY:
        return fields_spec

    expanded = {}
    prev = None
    for field in sorted(matched_fields):
        if _is_prefixed(field, prev):
            continue

        subspec = specular.doc_get(fields_spec, field)
        if subspec is None:
            raise InvalidInput(
                "illegal field '%s' in permission rules" % str(field))
        specular.doc_set(expanded, field, subspec)
        prev = field
    return expanded


def get_matched_allowed_fields(match):
    if isinstance(match.fields, doc.AnyPattern):
        return doc.ANY

    fields = match.fields.split(',')
    allowed_keys = set()
    for field in fields:
        allowed_keys.add(tuple(field.split(FIELD_SEPARATOR)))
    return allowed_keys


def make_fields_spec(context):
    fields_spec = {}
    for key, value in specular.iter_spec_artifacts(
            context, ('fields',), missing=Leaf, keys=True):
        if value is not Leaf:
            value = value['fields_spec']
        fields_spec[key] = value
    return fields_spec


@specular.make_constructor
def collection_constructor(context, loc, top_spec):
    value = {}
    value['collection_path'] = utils.mk_url_prefix(loc, top_spec)
    value['fields_spec'] = make_fields_spec(context)
    return value


@specular.make_constructor
def struct_constructor(context):
    return {'fields_spec': make_fields_spec(context)}


PERMISSIONS_CONSTRUCTORS = {
    '.collection': collection_constructor,
    '.field.struct': struct_constructor,
}


class Permissions(ProcessorFactory):
    Constructors = PERMISSIONS_CONSTRUCTORS

    COLUMNS = ('collection',
               'action',
               'role',
               'filter',
               'check',
               'fields',
               'comment')

    def __init__(self, collection_loc, action_name,
                 permission_rules, collection_path, fields_spec,
                 permissions_read, permissions_write, permissions_namespace,
                 permissions_mode, permissions_strict):

        rules_funcname = permission_rules
        rules = utils.import_object(rules_funcname)() if rules_funcname \
                else _default_rules

        self.fields_spec = fields_spec
        self.collection_path = collection_path
        self.action_name = action_name
        self.read_permissions_tag = permissions_read or action_name
        self.write_permissions_tag = permissions_write or action_name
        self.namespace = permissions_namespace
        mode = permissions_mode
        self.check_read = mode is None or mode == 'read'
        self.check_write = mode is None or mode == 'write'

        self.strict = permissions_strict is None or permissions_strict

        self.tab_rules = self.init_tab_rules(rules)

    def _parse_rules(self, rules):
        """
        Parse given rules and construct the appropriate segment patterns.

        Example:
            '*' => doc.ANY
        """
        parsed_rules = []
        nu_columns = len(self.COLUMNS)
        for rule in rules:
            if len(rule) != nu_columns:
                msg = ('Rules must consist of {!s} columns. An invalid rule'
                       ' found ({!r})')
                raise InvalidInput(msg.format(nu_columns, ','.join(rule)))
            parsed_rules.append([doc.parse_pattern(segment)
                                for segment in rule])
        return parsed_rules

    def init_tab_rules(self, rules):
        rules = self._parse_rules(rules)
        tab_rules = Tabmatch(self.COLUMNS)
        tab_rules.update(
            map((lambda x: tab_rules.Row(*x)), rules))
        return tab_rules

    def _get_pattern_set(self, collection, action, role):
        """
        Get all patterns set from request's runtime.

        Specifically, get groups to which user belongs, and action of request.
        """
        return [
                [collection],
                [action],
                [role],
                [doc.ANY],
                [doc.ANY],
                [doc.ANY],
                [doc.ANY],
        ]

    def load_object(self, name):
        if isinstance(name, doc.AnyPattern):
            return None
        prefix = '%s.' % self.namespace if self.namespace else ''
        full_name = prefix + name
        func = utils.import_object(full_name)
        if not callable(func):
            raise InvalidInput("Given object is not callable")
        return func

    def compute_permissions(self, collection, action_tag, role, runtime):
        pattern_set = self._get_pattern_set(collection, action_tag, role)
        expand_columns = {'filter', 'check', 'fields'}
        matches = list(self.tab_rules.multimatch(
            pattern_set, expand=expand_columns))
        if not matches:
            return {
                'enabled': False,
                'filter': None,
                'check': None,
                'fields': [],
            }

        if len(matches) > 1:
            raise InvalidInput("Multiple rules found!")

        match = matches[0]
        matched_filter = self.load_object(match.filter)
        matched_check = self.load_object(match.check)

        # As a final step, we save in the runtime the list of fields that
        # are allowed to be read or written.
        allowed_fields = get_matched_allowed_fields(match)
        expanded_fields = expand_paths(allowed_fields, self.fields_spec)
        return {
            'enabled': True,
            'filter': matched_filter,
            'check': matched_check,
            'fields': expanded_fields,
        }

    def process(self, runtime_data):
        runtime = runtime_data['$runtime']
        role = runtime_data.get('auth/role')

        result = {}
        if self.check_read:
            read_permissions = self.compute_permissions(
                self.collection_path, self.read_permissions_tag,
                role, runtime)

            if self.strict and not read_permissions['enabled']:
                raise AccessDeniedError(
                    'You do not have read permissions')

            add_prefixed(result, read_permissions, 'permissions/read/')

        if self.check_write:
            if self.check_read and \
               self.write_permissions_tag == self.read_permissions_tag:
                write_permissions = read_permissions
            else:
                write_permissions = self.compute_permissions(
                    self.collection_path, self.write_permissions_tag,
                    role, runtime)

            if self.strict and not write_permissions['enabled']:
                raise AccessDeniedError(
                    'You do not have write permissions')

            add_prefixed(result, write_permissions, 'permissions/write/')

        return result
