# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: api.py
@date: 3/9/2019
@desc:
'''

import json
import os
import time
from getpass import getuser

import numpy as np

import srfnef as nef
from srfnef.typing import make_dataclass, dataclass, DataClass, TYPE_BIND

schema_directory_path = '/home/bill52547/Workspace/SRF-NEF-DB/schema/'
api_directory_path = '/home/bill52547/Workspace/SRF-NEF-DB/APIs/'
resource_directory_path = '/home/bill52547/Workspace/SRF-NEF-DB/resources/'
tag_dict_path = api_directory_path + 'tags_dict.json'
schema0_path = schema_directory_path + 'schema.json'


def _get_schema_path(id_):
    if id_.startswith('schema'):
        return schema_directory_path + id_ + '.json'
    return schema_directory_path + 'schema_' + id_ + '.json'


def _get_api_path(id_):
    if id_.startswith('api_'):
        return api_directory_path + id_ + '.json'
    return api_directory_path + 'api_' + id_ + '.json'


def _get_resourece_path(id_):
    if id_.startswith('res_'):
        return api_directory_path + id_ + '.json'
    return resource_directory_path + 'res_' + id_ + '.hdf5'


def _get_task_path(id_):
    if id_.startswith('task_'):
        return api_directory_path + id_ + '.json'
    return api_directory_path + 'task_' + id_ + '.json'


def _update_hash(_hash: str, id_):
    with open(api_directory_path + 'hash_dict.json', 'r+') as fin:
        _hash_list = json.load(fin)
        if _hash in _hash_list.keys():
            id_ = _hash_list[_hash]
        else:
            _hash_list[_hash] = id_
            json.dump(_hash_list, fin)
    return id_


def _resource_hash(path: str):
    import hashlib

    if os.path.isdir(path):
        raise ValueError('Only file can be hashed')

    def hash_(path):
        BLOCKSIZE = 65536
        hasher = hashlib.sha1()

        with open(path, 'rb') as fin:
            buf = fin.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = fin.read(BLOCKSIZE)
        return hasher.hexdigest()

    file_hashes = hash_(path)
    return ''.join(file_hashes)


def _patch_npndarray_to_list():
    pass


def _search_id_with_tags(tags = None):
    with open(tag_dict_path, 'r') as fin:
        tag_dict = json.load(fin)
    ans = set()
    if tags is None:
        tags = tag_dict.keys()
    for tag in tags:
        if tag not in tag_dict.keys():
            raise ValueError(f'tag {tag} is not existing in tag_list')
        if not ans:
            ans = set(tag_dict[tag])
        else:
            ans = ans.intersection(tag_dict[tag])
    return list(ans)


def _post_tags(*, tags: (str, list, set), id_: str):
    if isinstance(tags, list):
        tags = set(tags)
    elif not isinstance(tags, set):
        tags = {tags}

    with open(tag_dict_path, 'r') as fin:
        tag_dict = json.load(fin)

    for tag in tags:
        if tag in tag_dict.keys():
            if id_ not in tag_dict[tag]:
                tag_dict[tag].append(id_)
        else:
            tag_dict[tag] = [id_]

    with open(tag_dict_path, 'w') as fout:
        json.dump(tag_dict, fout, indent = 4, separators = (',', ': '))


def _delete_tags(*, tags: (str, list, set) = None, id_: str):
    with open(tag_dict_path, 'r') as fin:
        tag_dict = json.load(fin)

    if tags is None:
        tags = tag_dict.keys()
    elif isinstance(tags, list):
        tags = set(tags)
    elif not isinstance(tags, set):
        tags = {tags}

    for tag in tags:
        if tag in tag_dict.keys():
            tag_dict[tag].remove(id_)

    with open(tag_dict_path, 'w') as fout:
        json.dump(tag_dict, fout, indent = 4, separators = (',', ': '))


def _parse_cls_to_schema(cls, *, tags = [], rewrite = True):
    schema_path = schema_directory_path + 'schema_' + cls.__name__ + '.json'
    if os.path.isfile(schema_path) and not rewrite:
        with open(schema_path, 'r') as fin:
            return json.load(fin)
    else:
        with open(schema0_path, 'r') as fin:
            _dct = json.load(fin)
        _dct['name'] = 'schema_' + cls.__name__
        _dct['family'] = cls.__name__
        _dct['tags'] = tags + [cls.__name__]
        _dct['tags'] = list(set(_dct['tags']))
        _dct['schema'] = 'schema'
        _metadata = {}
        try:
            for key, _cls in cls.__annotations__.items():
                if isinstance(_cls, DataClass):
                    _metadata.update({key: _parse_cls_to_schema(_cls).__name__})
                else:
                    _metadata.update({key: _cls.__name__})
        except:
            pass
        _dct['metadata'] = _metadata
        with open(schema_path, 'w') as fout:
            json.dump(_dct, fout, indent = 4, separators = (',', ': '))
        return _dct


def _parse_schema_to_cls(dct):
    if isinstance(dct, str):
        if dct.startswith('schema_'):
            with open(dct, 'r') as fin:
                dct = json.load(fin)
        else:
            ValueError(dct)
    else:
        assert isinstance(dct, dict) and 'family' in dct.keys()

    fields = []
    cls_name = dct['family']
    for key, val in dct.items():
        if key == 'classname':
            continue
        if isinstance(val, dict) and 'family' in val.keys():
            val = _parse_schema_to_cls(val)
        if val == 'list':
            val = 'numpy.ndarray'
        fields.append((key, val))
    try:
        return make_dataclass(cls_name, fields)
    except:
        ValueError(cls_name, fields)


def _parse_resource_to_api(resource = None, *, id_ = "", tags = []):
    if resource is None:
        with open(schema0_path, 'r') as fin:
            _dct = json.load(fin)
        cls_name = 'Undefined'
    else:
        assert isinstance(resource, DataClass)
        cls_name = resource.__class__.__name__
        try:
            schema_path = schema_directory_path + 'schema_' + cls_name + '.json'
            with open(schema_path, 'r') as fin:
                _dct = json.load(fin)
        except:
            _parse_cls_to_schema(resource.__class__)
            schema_path = schema_directory_path + 'schema_' + cls_name + '.json'
            with open(schema_path, 'r') as fin:
                _dct = json.load(fin)

    _metadata = {}

    if id_ == "":
        id_ = str(time.time()).replace('.', '')
        _dct['id'] = 'api_' + id_
    else:
        _dct['id'] = 'api_' + id_

    _dct['creationTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))
    _dct['tags'].extend(tags)
    _dct['tags'] = list(set(_dct['tags']))
    _dct['creator'] = getuser()
    _dct['family'] = cls_name
    _dct['schema'] = 'schema_' + cls_name
    name = _dct['name'] = 'api_' + cls_name
    res_path = _get_resourece_path(id_)
    if resource is not None:
        nef.save(res_path, resource)

    for key in _dct['metadata'].keys():
        val = getattr(resource, key)
        if isinstance(val, DataClass):
            _parse_resource_to_api(val, id_ = id_ + '_' + key, name = name + '/' + key,
                                   tags = tags)
            _metadata.update({key: _dct['id'] + '_' + key})
        elif key == 'data':
            _metadata.update({key: f'numpy.ndarray with shape{val.shape}'})
        elif isinstance(val, np.ndarray):
            _metadata.update({key: val.tolist()})
        else:
            _metadata.update({key: val})
    _dct['metadata'] = _metadata
    if resource is not None:
        _dct['diskSizeBytes'] = os.path.getsize(res_path)
        _dct['fingerprint'] = [_resource_hash(res_path)]
        _dct['sourceDisk'] = [res_path]
    api_path = _get_api_path(id_)
    with open(api_path, 'w') as fout:
        json.dump(_dct, fout, indent = 4, separators = (',', ': '))

    return _dct


def _parse_api_to_resource(dct):
    if isinstance(dct, str):
        if dct.startswith('api_'):
            with open(dct, 'r') as fin:
                dct = json.load(fin)
        else:
            ValueError(dct)
    else:
        assert isinstance(dct, dict) and 'family' in dct.keys()

    if dct['sourceDisk']:
        return nef.load(dct['sourceDisk'])
    cls = TYPE_BIND[json.load(fin)['family']]

    _dct = {}
    for key, val in dct['metadata'].items():
        if isinstance(val, dict) and 'family' in val.keys():
            _dct.update({key, _parse_api_to_resource(val)})
        else:
            _dct.update({key: val})

    return cls(**_dct)


@dataclass
class APIBackend:
    @staticmethod
    def GET(id_: str):
        try:
            api_path = _get_api_path(id_)
            with open(api_path, 'r') as fin:
                return json.load(fin)
        except:
            raise ValueError('file doesn\'t exist')

    @staticmethod
    def POST(resource: DataClass = None, tags = []):
        api = _parse_resource_to_api(resource, tags)
        _post_tags(tags = api['tags'], id_ = api['id'])
        return api

    @staticmethod
    def UPDATE(id_: str, **kwargs):
        api = APIBackend.GET(id_)
        if api['deletionProtection']:
            raise ValueError(f'API {id} cannot be deleted or updated.')
        all_tags = api['tags']
        api.update(kwargs)
        api_path = _get_api_path(id_)
        with open(api_path, 'w') as fin:
            json.dump(api, fin, indent = 4, separators = (',', ': '))
        if 'tags' in kwargs.keys():
            _delete_tags(tags = all_tags, id_ = id_)
            _post_tags(tags = api['tags'], id_ = api['id'])
        return api

    @staticmethod
    def DELETE(id_: str):
        print(f'API {id_} will be marked as DELETED')
        return APIBackend.UPDATE(id_, status = 'DELETED')

    @staticmethod
    def FORCE_DELETE(id_: str, *, force_deletion = False):
        if force_deletion:
            ValueError(f'if you REALLY want to remove api {id_}, set argument force_deletion = '
                       f'True')

        print(f'Warning: API {id_} and its corresponding resources are being deleted.')

        api = APIBackend.GET(id_)

        if api['deletionProtection']:
            raise ValueError(f'API {id_} is not deletable.')

        api_path = _get_api_path(id_)

        try:
            os.remove(api_path)
        except:
            print('removing file', api_path, 'failed')

        if not isinstance(api.sourceDisk, list):
            try:
                os.remove(api.sourceDisk)
            except:
                print('removing resource corresponding to api', id_, 'at', api.sourceDisk, 'failed')

        _delete_tags(id_ = id_)

    @staticmethod
    def LOCK(id_: str):
        return APIBackend.UPDATE(id_, deletionProjection = True)

    @staticmethod
    def SEARCH(*, tags: (str, list, set) = None):
        return _search_id_with_tags(tags)


@dataclass
class ResourceBackend:
    @staticmethod
    def GET(id_: str):
        api_path = _get_api_path(id_)
        if not os.path.isfile(api_path):
            raise ValueError('file', api_path, ' doesn\'t exist')
        api = APIBackend.GET(id_)
        out = []
        for path in api['sourceDisk']:
            out.append(nef.load(path))
        return out if len(out) > 1 else out[0]

    @staticmethod
    def POST(resource, tags = []):
        return _parse_resource_to_api(resource, tags)

    @staticmethod
    def ADD(*, res_id, api_id):
        api = APIBackend.GET(api_id)
        res_api = APIBackend.GET(res_id)
        sourceDisk = api['sourceDisk'] + res_api['sourceDisk']
        fingerprint = api['fingerprint'] + res_api['fingerprint']
        diskSizeBytes = api['diskSizeBytes'] + res_api['diskSizeBytes']

        APIBackend.UPDATE(
            {'sourceDisk': sourceDisk, 'fingerprint': fingerprint, 'diskSizeBytes': diskSizeBytes})
        return APIBackend.GET(api_id)


@dataclass
class TaskBackend(APIBackend):
    @staticmethod
    def RUN(id_: str):
        api = APIBackend.GET(id_)
        args = []
        for ind, id__ in enumerate(api['sourceDisk']):
            if ind == 0:
                api_ = APIBackend.GET(id__)
                # if not api_.functionality.callable:
                #     raise ValueError(f'Resource from api {id__} is not callable')
                if len(api_['sourceDisk']) > 1:
                    raise NotImplementedError
                func = nef.load(api_['sourceDisk'][0])
            else:
                api_ = APIBackend.GET(id__)
                if not isinstance(api_['sourceDisk'], list):
                    raise NotImplementedError
                if len(api_['sourceDisk']) > 1:
                    raise NotImplementedError
                arg = nef.load(api_['sourceDisk'][0])
                args.append(arg)
        out = func(*args)
        _api = ResourceBackend.POST(out)
        print('Task', api['id'], 'finished, with output', _api['id'])
        return _api['id']

    @staticmethod
    def BUILD(*, func_id: str, args_id: (list, str), tags = []):
        api = APIBackend.POST(tags = tags)
        if isinstance(args_id, list):
            args = [func_id] + args_id
        else:
            args = [func_id, args_id]
        APIBackend.UPDATE(api['id'], sourceDisk = args, tags = ['Task'])
        return api
