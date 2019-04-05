apimas_schemata = [
    ('.boolean',
     {'.boolean': {}}),

    ('.string',
     {'.string': {}}),

    ('.integer',
     {'.integer': {}}),

    ('.float',
     {'.float': {}}),

    ('.processor',
     {'.processor': {},
      'module_path': {'.string': {}},
      'read_keys': {},
      'write_keys': {},
     }),

    ('.flag',
     {'.flag': {}}),

    ('.flag.nowrite',
     {'.flag.nowrite': {}}),

    ('.flag.noread',
     {'.flag.noread': {}}),

    ('.flag.noupdate',
     {'.flag.noupdate': {}}),

    ('.flag.nullable',
     {'.flag.nullable': {}}),

    ('.flag.nullable.default',
     {'.flag.nullable.default': {},
      'default': {'=': None}}),

    ('.flag.filterable',
     {'.flag.filterable': {}}),

    ('.flag.orderable',
     {'.flag.orderable': {}}),

    ('.flag.searchable',
     {'.flag.searchable': {}}),

    ('.field',
     {
         '.field': {},
         'source': {'.string': {}},
         '.flag': {},
         'default': {},
         'default_fn': {'.string': {}},
     }),

    ('.field.string',
     {'.field.string': {},
      'default': {'.string': {}}}),

    ('.field.serial',
     {'.field.serial': {},
      '.flag.nowrite': {}}),

    ('.field.integer',
     {'.field.integer': {}}),

    ('.field.float',
     {'.field.float': {}}),

    ('.field.decimal',
     {'.field.decimal': {},
      ':decimal_places': {'.integer': {}}}),

    ('.field.ref',
     {'.field.ref': {},
      ':root_url': {'.string': {}},
      'to': {'.string': {}}}),

    ('.field.identity',
     {'.field.identity': {},
      ':root_url': {'.string': {}},
      'to': {'.string': {}}}),

    ('.field.uuid',
     {'.field.uuid': {}}),

    ('.field.text',
     {'.field.text': {}}),

    ('.field.email',
     {'.field.email': {}}),

    ('.field.boolean',
     {'.field.boolean': {},
      'default': {'.boolean': {}}}),

    ('.field.datetime',
     {'.field.datetime': {}}),

    ('.field.date',
     {'.field.date': {}}),

    ('.field.file',
     {'.field.file': {}}),

    ('.field.choices',
     {'.field.choices': {},
      'allowed': {},
      'displayed': {}}),

    ('.field.struct',
     {
         '.field.struct': {},
         'fields': {'?': {'.field': {}}},
     }),

    ('.action',
     {
         '.action': {},
         'on_collection': {'.boolean': {}},
         'processors': {'?': {'.processor': {}}},
     }),

    ('.action-template',
     {
         '.action-template': {},
         '?': {'.action': {}},
     }),

    ('.collection',
     {
         '.collection': {},
         'id_field': {'.string': {}},
         'flat': {'.boolean': {}},
         'actions': {
             '.action-template': {},
             '?': {'.action': {}},
         },
         'fields': {'?': {".field": {}}},
     }),

    ('.field.collection',
     {
         '.field.collection': {},
         '.collection': {},
     }),

    ('.endpoint',
     {
         '.endpoint': {},
         'prefix': {'.string': {}},
         'collections': {
             '?': {'.collection': {}},
         },
     }),

    ('.apimas_app',
     {
         '.apimas_app': {},
         'endpoints': {
             '?': {'.endpoint': {}},
         },
     }),

    ('.processor.permissions',
     {
         '.processor.permissions': {},
         'module_path': 'apimas.components.permissions.Permissions',
         ':permission_rules': {'.string': {}},
         ':permissions_namespace': {'.string': {}},
         ':permissions_mode': {'.string': {}},
         ':permissions_strict': {'.boolean': {}},
         ':permissions_read': {'.string': {}},
         ':permissions_write': {'.string': {}},
     }),

    ('.processor.permissions.readwrite',
     {
         '.processor.permissions.readwrite': {},
         'read_keys': {'=': ('auth/role',)},
         'write_keys': {'=': (
             'permissions/write/enabled',
             'permissions/write/filter',
             'permissions/write/check',
             'permissions/write/fields',
             'permissions/read/enabled',
             'permissions/read/filter',
             'permissions/read/check',
             'permissions/read/fields',
         )},
     }),

    ('.processor.permissions.write',
     {
         '.processor.permissions.write': {},
         'read_keys': {'=': ('auth/role',)},
         'write_keys': {'=': (
             'permissions/write/enabled',
             'permissions/write/filter',
             'permissions/write/check',
             'permissions/write/fields',
         )},
         ':permissions_mode': 'write',
     }),

    ('.processor.permissions.read',
     {
         '.processor.permissions.read': {},
         'read_keys': {'=': ('auth/role',)},
         'write_keys': {'=': (
             'permissions/read/enabled',
             'permissions/read/filter',
             'permissions/read/check',
             'permissions/read/fields',
         )},
         ':permissions_mode': 'read',
     }),

    ('.processor.permissions.read.nonstrict',
     {
         '.processor.permissions.read.nonstrict': {},
         ':permissions_strict': False,
     }),


    ('.processor.authentication',
     {
         '.processor.authentication': {},
         'module_path': 'apimas.components.auth.Authentication',
         'read_keys': {'=': (
             'request/meta/headers',
             # 'response/meta/headers',
         )},
         'write_keys': {'=': (
             'auth/identity',
             # 'response/meta/headers',
         )},
         ':authenticator': {'.string': {}},
         ':verifier': {'.string': {}},
     }),

    ('.processor.user_retrieval',
     {
         '.processor.user_retrieval': {},
         'module_path': 'apimas.components.auth.UserRetrieval',
         'read_keys': {'=': (
             'request/meta/headers',
             'auth/identity',
         )},
         'write_keys': {'=': (
             'auth/user',
             'auth/role',
         )},
         ':user_resolver': {'.string': {}},
     }),

    ('.processor.import_write_data',
     {
         '.processor.import_write_data': {},
         'module_path': 'apimas.components.impexp.ImportWriteData',
         'read_keys': {'=': (
             'request/content',
             'permissions/write/enabled',
             'permissions/write/fields',
         )},
         'write_keys': {'=': (
             'imported/content',
         )},
     }),

    ('.processor.import_params',
     {
         '.processor.import_params': {},
         'module_path': 'apimas.components.impexp.ImportParams',
         'read_keys': {'=': (
             'request/meta/params',
             'permissions/read/fields',
         )},
         'write_keys': {'=': (
             'imported/filters',
             'imported/ordering',
             'imported/search',
             'imported/pagination',
         )},
         ':filter_compat': {'.boolean': {}},
         ':ordering_compat': {'.boolean': {}},
     }),

    ('.processor.export_data',
     {
         '.processor.export_data': {},
         'module_path': 'apimas.components.impexp.ExportData',
         'read_keys': {'=': (
             'exportable/content',
             'exportable/meta',
             'permissions/read/fields',
         )},
         'write_keys': {'=': (
             'response/content',
         )},
     }),

    ('.runtime', {'.runtime': {}}),
]
