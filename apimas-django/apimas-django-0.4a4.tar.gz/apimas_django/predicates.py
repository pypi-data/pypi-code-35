import specular
from apimas.predicates import apimas_schemata

apimas_django_schemata = [
    ('.collection.django',
     {
         '.collection.django': {},
         'model': {'.string': {}},
         'subset': {'.string': {}},
         'bound': {'.string': {}},
     }),

    ('.field.collection.django',
     {
         '.field.collection.django': {},
         '.collection.django': {},
     }),

    ('.processor.transaction_begin',
     {
         '.processor.transaction_begin': {},
         'module_path': 'apimas_django.db.BeginTransaction',
         'read_keys': {'=': ()},
         'write_keys': {'=': (
             'guards/transaction_begin',
         )},
     }),

    ('.processor.transaction_commit',
     {
         '.processor.transaction_commit': {},
         'module_path': 'apimas_django.db.CommitTransaction',
         'read_keys': {'=': (
             'guards/transaction_begin',
             'backend/checked_response',
         )},
         'write_keys': {'=': (
             'guards/transaction_commit',
         )},
     }),

    ('.processor.assume_checked',
     {
         '.processor.assume_checked': {},
         'module_path': 'apimas_django.permissions.AssumeChecked',
         'read_keys': {'=': (
             'backend/raw_response',
         )},
         'write_keys': {'=': (
             'backend/checked_response',
         )},
     }),

    ('.processor.filtered_as_selected',
     {
         '.processor.filtered_as_selected': {},
         'module_path': 'apimas_django.permissions.FilteredAsSelected',
         'read_keys': {'=': (
             'backend/filtered_response',
         )},
         'write_keys': {'=': (
             'backend/selected_response',
         )},
     }),

    ('.processor.instance_to_dict',
     {
         '.processor.instance_to_dict': {},
         'module_path': 'apimas_django.processors.InstanceToDict',
         'read_keys': {'=': (
             'backend/checked_response',
         )},
         'write_keys': {'=': (
             'exportable/content',
         )},
     }),

    ('.processor.instance_to_dict_committed',
     {
         '.processor.instance_to_dict_committed': {},
         'module_path': 'apimas_django.processors.InstanceToDict',
         'read_keys': {'=': (
             'backend/checked_response',
             'guards/transaction_commit',
         )},
         'write_keys': {'=': (
             'exportable/content',
         )},
     }),

    ('.processor.response_handler',
     {
         '.processor.response_handler': {},
         'module_path': 'apimas_django.processors.ResponseHandler',
         'read_keys': {'=': (
             'backend/checked_response',
         )},
         'write_keys': {'=': ()},
         ':response_handler': {'.string': {}},
     }),

    ('.processor.filtering',
     {
         '.processor.filtering': {},
         'module_path': 'apimas_django.filtering.Filtering',
         'read_keys': {'=': (
             'imported/filters',
             'backend/filtered_response',
         )},
         'write_keys': {'=': (
             'backend/filtered_response',
         )},
     }),

    ('.processor.ordering',
     {
         '.processor.ordering': {},
         'module_path': 'apimas_django.ordering.Ordering',
         'read_keys': {'=': (
             'imported/ordering',
             'backend/filtered_response',
         )},
         'write_keys': {'=': (
             'backend/ordered_response',
         )},
     }),

    ('.processor.search',
     {
         '.processor.search': {},
         'module_path': 'apimas_django.search.Search',
         'read_keys': {'=': (
             'imported/search',
             'backend/filtered_response',
         )},
         'write_keys': {'=': (
             'backend/filtered_response',
         )},
     }),

    ('.processor.pagination',
     {
         '.processor.pagination': {},
         'module_path': 'apimas_django.pagination.Pagination',
         'read_keys': {'=': (
             'imported/pagination',
             'backend/ordered_response',
             'exportable/meta',
         )},
         'write_keys': {'=': (
             'backend/selected_response',
             'exportable/meta',
         )},
         ':pagination_default_limit': {'.integer': {}},
     }),

    ('.processor.object_retrieval_for_update',
     {
         '.processor.object_retrieval_for_update': {},
         'module_path': 'apimas_django.permissions.ObjectRetrievalForUpdate',
         'read_keys': {'=': (
             'request/meta/kwargs',
             'permissions/write/filter',
             'guards/transaction_begin',
         )},
         'write_keys': {'=': (
             'backend/instance',
         )},
     }),

    ('.processor.load_data',
     {
         '.processor.load_data': {},
         'module_path': 'apimas_django.loaddata.LoadData',
         ':loaddata_full': {'.boolean': {}},
     }),

    ('.processor.load_data.noinstance',
     {
         '.processor.load_data.noinstance': {},
         'read_keys': {'=': (
             'imported/content',
             'guards/transaction_begin',
         )},
         'write_keys': {'=': (
             'backend/input',
         )},
     }),

    ('.processor.load_data.instance',
     {
         '.processor.load_data.instance': {},
         'read_keys': {'=': (
             'imported/content',
             'backend/instance',
             'guards/transaction_begin',
         )},
         'write_keys': {'=': (
             'backend/input',
         )},
     }),

    ('.processor.load_data.instance.partial',
     {
         '.processor.load_data.instance.partial': {},
         ':loaddata_full': False,
     }),

    ('.processor.response_filtering_resource',
     {
         '.processor.response_filtering_resource': {},
         'module_path': 'apimas_django.permissions.FilterResourceResponse',
         'read_keys': {'=': (
             'backend/raw_response',
             'request/meta/kwargs',
             'permissions/read/filter',
         )},
         'write_keys': {'=': (
             'backend/filtered_response',
         )},
         ':filter_resource_strict': {'.boolean': {}},
     }),

    ('.processor.response_filtering_resource.strict',
     {
         '.processor.response_filtering_resource.strict': {},
         'module_path': 'apimas_django.permissions.FilterResourceResponse',
         ':filter_resource_strict': True,
     }),

    ('.processor.response_filtering_collection',
     {
         '.processor.response_filtering_collection': {},
         'module_path': 'apimas_django.permissions.FilterCollectionResponse',
         'read_keys': {'=': (
             'backend/raw_response',
             'permissions/read/filter',
         )},
         'write_keys': {'=': (
             'backend/filtered_response',
         )},
     }),

    ('.processor.write_permission_check',
     {
         '.processor.write_permission_check': {},
         'module_path': 'apimas_django.permissions.WritePermissionCheck',
         'write_keys': {'=': (
             'guards/write_check',
         )},
     }),

    ('.processor.write_permission_check.instance',
     {
         '.processor.write_permission_check.instance': {},
         'read_keys': {'=': (
             'backend/input',
             'backend/instance',
             'permissions/write/check',
         )},
     }),

    ('.processor.write_permission_check.noinstance',
     {
         '.processor.write_permission_check.noinstance': {},
         'read_keys': {'=': (
             'backend/input',
             'permissions/write/check',
         )},
     }),

    ('.processor.read_permission_check',
     {
         '.processor.read_permission_check': {},
         'module_path': 'apimas_django.permissions.ReadPermissionCheck',
         'read_keys': {'=': (
             'backend/selected_response',
             'permissions/read/check',
         )},
         'write_keys': {'=': (
             'backend/checked_response',
         )},
         ':read_check_strict': {'.boolean': {}},
     }),

    ('.processor.read_permission_check.strict',
     {
         '.processor.read_permission_check.strict': {},
         'module_path': 'apimas_django.permissions.ReadPermissionCheck',
         ':read_check_strict': True,
     }),

    ('.processor.handler',
     {'.processor.handler': {}}),

    ('.processor.handler.create',
     {
         '.processor.handler.create': {},
         'module_path': 'apimas_django.handlers.CreateHandler',
         'read_keys': {'=': (
             'request/meta/kwargs',
             'backend/input',
             'guards/write_check',
         )},
         'write_keys': {'=': (
             'backend/raw_response',
         )},
         ':custom_create_handler': {'.string': {}},
     }),

    ('.processor.handler.list',
     {
         '.processor.handler.list': {},
         'module_path': 'apimas_django.handlers.ListHandler',
         'read_keys': {'=': (
             'request/meta/kwargs',
             # 'backend/input',
         )},
         'write_keys': {'=': (
             'backend/raw_response',
         )},
     }),

    ('.processor.handler.retrieve',
     {
         '.processor.handler.retrieve': {},
         'module_path': 'apimas_django.handlers.RetrieveHandler',
         'read_keys': {'=': (
             'request/meta/kwargs',
             # 'backend/input',
             # 'backend/instance',
         )},
         'write_keys': {'=': (
             'backend/raw_response',
         )},
     }),

    ('.processor.handler.update',
     {
         '.processor.handler.update': {},
         'module_path': 'apimas_django.handlers.UpdateHandler',
         'read_keys': {'=': (
             'request/meta/kwargs',
             'guards/write_check',
             'backend/input',
             'backend/instance',
         )},
         'write_keys': {'=': (
             'backend/raw_response',
         )},
         ':custom_update_handler': {'.string': {}},
     }),

    ('.processor.handler.delete',
     {
         '.processor.handler.delete': {},
         'module_path': 'apimas_django.handlers.DeleteHandler',
         'read_keys': {'=': (
             'request/meta/kwargs',
             'backend/instance',
         )},
         'write_keys': {'=': (
             'backend/raw_response',
         )},
     }),

    ('.action.django',
     {
         '.action.django': {},
         'method': {'.string': {}},
         'status_code': {'.integer': {}},
         'content_type': {'.string': {}},
         'url': {'.string': {}},
     }),

    ('.action.django.recipe', {'.action.django.recipe': {}}),

    ('.action-template.django', {'.action-template.django': {}}),

    ('.action-template.django.create',
     {
         '.action-template.django.create': {},
         'create': {
             '.action.django': {},
             'method': 'POST',
             'status_code': 201,
             'content_type': 'application/json',
             'on_collection': False,
             ':permissions_read': 'retrieve',
             'url': '/',
             'processors': [
                 {'.processor.authentication': {}},
                 {'.processor.user_retrieval': {}},
                 {'.processor.permissions.write': {}},
                 {'.processor.import_write_data': {}},
                 {'.processor.transaction_begin': {}},
                 {'.processor.load_data.noinstance': {}},
                 {'.processor.write_permission_check.noinstance': {}},
                 {'.processor.handler.create': {}},
                 {'.processor.permissions.read.nonstrict': {}},
                 {'.processor.response_filtering_resource': {}},
                 {'.processor.filtered_as_selected': {}},
                 {'.processor.read_permission_check': {}},
                 {'.processor.transaction_commit': {}},
                 {'.processor.instance_to_dict_committed': {}},
                 {'.processor.export_data': {}},
             ],
         },
     },
    ),

    ('.action.django.recipe.list',
     {
         '.action.django.recipe.list': {},
         'content_type': 'application/json',
         'on_collection': True,
         'processors': [
             {'.processor.authentication': {}},
             {'.processor.user_retrieval': {}},
             {'.processor.permissions.read': {}},
             {'.processor.import_params': {}},
             {'.processor.handler.list': {}},
             {'.processor.response_filtering_collection': {}},
             {'.processor.filtering': {}},
             {'.processor.search': {}},
             {'.processor.ordering': {}},
             {'.processor.pagination': {}},
             {'.processor.read_permission_check': {}},
             {'.processor.instance_to_dict': {}},
             {'.processor.export_data': {}},
         ],
     },
    ),

    ('.action-template.django.list',
     {
         '.action-template.django.list': {},
         'list': {
             '.action.django.recipe.list': {},
             'method': 'GET',
             'status_code': 200,
             'url': '/',
         },
     },
    ),

    ('.action.django.recipe.handle_collection',
     {
         '.action.django.recipe.handle_collection': {},
         'on_collection': True,
         'processors': [
             {'.processor.authentication': {}},
             {'.processor.user_retrieval': {}},
             {'.processor.permissions.read': {}},
             {'.processor.import_params': {}},
             {'.processor.handler.list': {}},
             {'.processor.response_filtering_collection': {}},
             {'.processor.filtering': {}},
             {'.processor.search': {}},
             {'.processor.ordering': {}},
             {'.processor.pagination': {}},
             {'.processor.read_permission_check': {}},
             {'.processor.response_handler': {}},
         ],
     },
    ),

    ('.action-template.django.retrieve',
     {
         '.action-template.django.retrieve': {},
         'retrieve': {
             '.action.django': {},
             'method': 'GET',
             'status_code': 200,
             'content_type': 'application/json',
             'on_collection': False,
             'url': '/*/',
             'processors': [
                 {'.processor.authentication': {}},
                 {'.processor.user_retrieval': {}},
                 {'.processor.permissions.read': {}},
                 {'.processor.handler.retrieve': {}},
                 {'.processor.response_filtering_resource.strict': {}},
                 {'.processor.filtered_as_selected': {}},
                 {'.processor.read_permission_check.strict': {}},
                 {'.processor.instance_to_dict': {}},
                 {'.processor.export_data': {}},
             ],
         },
     },
    ),

    ('.action.django.recipe.handle_instance',
     {
         '.action.django.recipe.handle_instance': {},
         'on_collection': False,
         'processors': [
             {'.processor.authentication': {}},
             {'.processor.user_retrieval': {}},
             {'.processor.permissions.read': {}},
             {'.processor.handler.retrieve': {}},
             {'.processor.response_filtering_resource.strict': {}},
             {'.processor.filtered_as_selected': {}},
             {'.processor.read_permission_check.strict': {}},
             {'.processor.response_handler': {}},
         ],
     },
    ),

    ('.action.django.recipe.partial_update',
     {
         '.action.django.recipe.partial_update': {},
         'content_type': 'application/json',
         'on_collection': False,
         ':permissions_read': 'retrieve',
         'processors': [
             {'.processor.authentication': {}},
             {'.processor.user_retrieval': {}},
             {'.processor.permissions.write': {}},
             {'.processor.import_write_data': {}},
             {'.processor.transaction_begin': {}},
             {'.processor.object_retrieval_for_update': {}},
             {'.processor.load_data.instance.partial': {}},
             {'.processor.write_permission_check.instance': {}},
             {'.processor.handler.update': {}},
             {'.processor.permissions.read.nonstrict': {}},
             {'.processor.response_filtering_resource': {}},
             {'.processor.filtered_as_selected': {}},
             {'.processor.read_permission_check': {}},
             {'.processor.transaction_commit': {}},
             {'.processor.instance_to_dict_committed': {}},
             {'.processor.export_data': {}},
         ],
     },
    ),

    ('.action-template.django.partial_update',
     {
         '.action-template.django.partial_update': {},
         'partial_update': {
             '.action.django.recipe.partial_update': {},
             'method': 'PATCH',
             'status_code': 200,
             'url': '/*/',
         },
     },
    ),

    ('.action-template.django.update',
     {
         '.action-template.django.update': {},
         'update': {
             '.action.django': {},
             'method': 'PUT',
             'status_code': 200,
             'content_type': 'application/json',
             'on_collection': False,
             ':permissions_read': 'retrieve',
             'url': '/*/',
             'processors': [
                 {'.processor.authentication': {}},
                 {'.processor.user_retrieval': {}},
                 {'.processor.permissions.write': {}},
                 {'.processor.import_write_data': {}},
                 {'.processor.transaction_begin': {}},
                 {'.processor.object_retrieval_for_update': {}},
                 {'.processor.load_data.instance': {}},
                 {'.processor.write_permission_check.instance': {}},
                 {'.processor.handler.update': {}},
                 {'.processor.permissions.read.nonstrict': {}},
                 {'.processor.response_filtering_resource': {}},
                 {'.processor.filtered_as_selected': {}},
                 {'.processor.read_permission_check': {}},
                 {'.processor.transaction_commit': {}},
                 {'.processor.instance_to_dict_committed': {}},
                 {'.processor.export_data': {}},
             ],
         },
     },
    ),

    ('.action-template.django.delete',
     {
         '.action-template.django.delete': {},
         'delete': {
             '.action.django': {},
             'method': 'DELETE',
             'status_code': 204,
             'content_type': 'application/json',
             'on_collection': False,
             'url': '/*/',
             'processors': [
                 {'.processor.authentication': {}},
                 {'.processor.user_retrieval': {}},
                 {'.processor.permissions.write': {}},
                 {'.processor.transaction_begin': {}},
                 {'.processor.object_retrieval_for_update': {}},
                 {'.processor.handler.delete': {}},
                 {'.processor.assume_checked': {}},
                 {'.processor.transaction_commit': {}},
             ],
         },
     },
    ),

    ('.runtime.django',
     {
         '.runtime.django': {},
         'request': {
             'content': {},
             'native': {},
             'meta': {
                 'params': {},
                 'files': {},
                 'headers': {},
                 'kwargs': {},
             },
         },
         'auth': {
             'identity': {},
             'user': {},
             'role': {},
         },
         'permissions': {
             'read': {
                 'enabled': {},
                 'fields': {},
                 'filter': {},
                 'check': {},
             },
             'write': {
                 'enabled': {},
                 'fields': {},
                 'filter': {},
                 'check': {},
             },
         },
         'imported': {
             'content': {},
             'filters': {},
             'ordering': {},
             'search': {},
             'pagination': {},
         },
         'guards': {
             'write_check': {},
             'transaction_begin': {},
             'transaction_commit': {},
         },
         'backend': {
             'instance': {},
             'input': {},
             'raw_response': {},
             'filtered_response': {},
             'ordered_response': {},
             'selected_response': {},
             'checked_response': {},
         },
         'exportable': {
             'content': {},
             'meta': {},
         },
         'response': {
             'content': {},
             'meta': {
                 'content_type': {},
                 'status_code': {},
                 'headers': {},
             },
         },
     },
    ),
]


domain = specular.Spec()
domain.compile_schemata(apimas_schemata)
domain.compile_schemata(apimas_django_schemata)
