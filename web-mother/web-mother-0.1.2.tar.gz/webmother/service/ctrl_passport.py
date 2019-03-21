# coding:utf-8

from webmother.db import mongo as db
from tweb.error_exception import ErrException, ERROR
from tweb import time
from bson.objectid import ObjectId
from webmother.service import ctrl_catalog, ctrl_org
from webmother.service.passport import Passport


def get_passport_tpl(cid, *auth_args):
    c = ctrl_catalog.read(cid, *auth_args)

    # 授权检查
    Passport().verify(*auth_args).operable(c.get('node'), 'grant.create')
    # END

    return Passport().json


def passport_create(cid, oid, passport_json, *auth_args):
    """
    分类与组织建立绑定关系
    :param cid: 分类节点ID
    :param oid: 组织ID
    :param passport_json: 授权描述信息
    :param auth_args: 鉴权参数：(signed, nonce), 即("签名的授权字符串", "临时一致性标示，需与生成签名时使用的nonce相同")
    :return:
    """
    c = ctrl_catalog.read(cid, *auth_args)

    # 授权检查
    pp = Passport().verify(*auth_args).operable(c.get('node'), 'grant.create')
    # END

    with db.start_session() as s:
        s.start_transaction()
        # begin
        node = c['node']
        cursor = db.catalog2org.find({'org': ObjectId(oid)}, {'org': 0})
        for item in cursor:
            other = item['catalog_node']
            # 如果已经授权或者授权给父节点，则无需再授权
            if node.find(other) == 0:
                raise ErrException(ERROR.E40020, extra=f'org({oid}) has got passport at catalog({other})')

            # 如果已经授权该组织给下级节点，则首先删除，再添加（相当于移动，升级到更高级资源节点）
            if other.find(node) == 0:
                db.catalog2org.delete_one({'catalog': item['catalog'], 'org': ObjectId(oid)})

        now = time.millisecond()
        db.catalog2org.insert_one({
            "catalog": ObjectId(cid),
            "catalog_node": node,
            "org": ObjectId(oid),
            "passport": Passport().update(node, oid, passport_json, pp).text,
            "created": now,
            "updated": now
        })
        # end
        s.commit_transaction()

    return _passport_read(cid, oid)


def passport_read(cid, oid, *auth_args):
    c = ctrl_catalog.read(cid, *auth_args)

    # 授权检查
    Passport().verify(*auth_args).operable(c.get('node'), 'grant.read')
    # END

    return _passport_read(cid, oid)


def _passport_read(cid, oid):
    c2o = db.catalog2org.find_one({'catalog': ObjectId(cid), 'org': ObjectId(oid)}, {'_id': 0})
    if c2o is None:
        raise ErrException(ERROR.E40400)

    c2o['catalog'] = c2o['catalog'].__str__()
    c2o['org'] = ctrl_org.simple_read(c2o['org'])
    c2o['passport'] = Passport().parse(c2o['passport']).json

    return c2o


def passport_update(cid, oid, passport_json, *auth_args):
    """
    更新组织对分类以及分类下资源的授权
    :param cid: 分类节点ID
    :param oid: 组织ID
    :param passport_json: 授权描述信息
    :param auth_args: 鉴权参数：(signed, nonce), 即("签名的授权字符串", "临时一致性标示，需与生成签名时使用的nonce相同")
    :return:
    """
    c = ctrl_catalog.read(cid, *auth_args)

    # 授权检查
    pp = Passport().verify(*auth_args).operable(c.get('node'), 'grant.update')
    # END

    c2o = db.catalog2org.find_one({'catalog': ObjectId(cid), 'org': ObjectId(oid)})
    if c2o is None:
        raise ErrException(ERROR.E40400)

    temp = dict()
    temp['passport'] = Passport().parse(c2o.get('passport')).update(c['node'], oid, passport_json, pp).text
    temp['updated'] = time.millisecond()
    db.catalog2org.update_one({'_id': c2o['_id']}, {'$set': temp})

    return _passport_read(cid, oid)


def passport_remove(cid, oid, *auth_args):
    """
    解除分类与组织的关系
    :param cid: 分类节点ID
    :param oid: 组织ID
    :param auth_args: 鉴权参数：(signed, nonce), 即("签名的授权字符串", "临时一致性标示，需与生成签名时使用的nonce相同")
    :return:
    """
    c = ctrl_catalog.read(cid, *auth_args)

    # 授权检查
    Passport().verify(*auth_args).operable(c.get('node'), 'grant.remove')
    # END

    # 使已签名的授权无效
    Passport.invalidate_signed(c['node'], oid)

    db.catalog2org.delete_one({'catalog': ObjectId(cid), 'org': ObjectId(oid)})

    return {}


def passports_query(cid, *auth_args):
    """
    获取分类节点的被授权的组织列表
    :param cid:
    :param auth_args: 鉴权参数：(signed, nonce), 即("签名的授权字符串", "临时一致性标示，需与生成签名时使用的nonce相同")
    :return:
    """
    c = ctrl_catalog.read(cid, *auth_args)

    # 授权检查
    Passport().verify(*auth_args).operable(c.get('node'), 'grant.read')
    # END

    cursor = db.catalog2org.find({'catalog': ObjectId(cid)}, {'_id': 0, 'catalog': 0})
    array = list()
    for item in cursor:
        item['org'] = ctrl_org.simple_read(item['org'])
        item['passport'] = Passport().parse(item['passport']).json
        array.append(item)

    return array
