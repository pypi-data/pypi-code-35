# coding:utf-8

from webmother.db import mongo as db
from tweb.json_util import filter_keys
from tweb.error_exception import ErrException, ERROR
from tweb import time
from bson.objectid import ObjectId
from webmother.service.passport import Passport
import re


# 分类节点状态以及状态迁移定义
class Status:
    removed = -10  # 已删除
    editing = 0  # 编辑中
    auditing = 10  # 待审(审核中)
    sleeping = 20  # 休眠中
    activated = 30  # 已激活

    status_map = {
        editing: {'submit': auditing, 'remove': removed},
        auditing: {'reject': editing, 'audit': sleeping, 'remove': removed},
        sleeping: {'activate': activated, 'remove': removed},
        activated: {'deactivate': sleeping}
    }

    @staticmethod
    def trans(cur_status, action):
        """
        在当前状态，进行操作将会得到新的状态
        :param cur_status: 当前状态
        :param action: 操作名称
        :return: 新的状态
        """

        valid_actions = Status.status_map.get(cur_status)
        if valid_actions is None:
            raise ErrException(ERROR.E40022, extra=f'current status is {cur_status}, forbid change status')

        new_status = valid_actions.get(action)
        if new_status is None:
            raise ErrException(ERROR.E40022, extra=f'current status is {cur_status}, wrong action [{action}]')

        return new_status


def create(cid, cata_meta, *auth_args):
    """
    向cid节点中添加cata_meta描述的子节点
    """
    c = simple_read(cid)

    # 授权检查
    Passport().verify(*auth_args).operable(c.get('node'), 'catalog.create')
    # END

    name = cata_meta.pop('name').lower()
    if not re.match(r'^[\w]{0,19}$', name):
        raise ErrException(ERROR.E40000, extra='name should be letter, number, _, and beginning with letter')

    cata_meta['node'] = '{}/{}'.format(c['node'], name)
    cata_meta['parent'] = ObjectId(cid)

    if db.catalog.find_one({'node': cata_meta['node'], 'status': {'$gte': 0}}) is not None:
        raise ErrException(ERROR.E40020)

    cata_meta['status'] = Status.editing
    now = time.millisecond()
    cata_meta['created'] = now
    cata_meta['updated'] = now

    result = db.catalog.insert_one(cata_meta)
    return simple_read(result.inserted_id)


def read(cid, *auth_args):
    c = simple_read(cid)

    # 授权检查
    Passport().verify(*auth_args).operable(c.get('node'), 'catalog.read')
    # END

    return c


def simple_read(cid, raw=False):
    if not ObjectId.is_valid(cid):
        raise ErrException(ERROR.E40000, extra='invalid cid %s' % cid)

    c = db.catalog.find_one({'_id': ObjectId(cid), 'status': {'$gte': 0}})
    if c is None:
        raise ErrException(ERROR.E40400, extra=f'the catalog({cid}) not existed')

    if not raw:
        c['name'] = c['node'].split('/').pop()
        c['cid'] = c.pop('_id').__str__()
        if 'parent' in c:
            c['parent'] = c['parent'].__str__()

    return c


def update(cid, cata_meta, *auth_args):
    """
    :param cid: 分类节点id
    :param cata_meta: 分类节点信息
    :param auth_args: 鉴权参数：(signed, nonce), 即("签名的授权字符串", "临时一致性标示，需与生成签名时使用的nonce相同")
    :return:
    """

    c = read(cid, *auth_args)

    # 授权检查
    Passport().verify(*auth_args).operable(c.get('node'), 'catalog.update')
    # END

    if c['status'] not in (Status.editing, Status.auditing, Status.sleeping, Status.activated):
        raise ErrException(ERROR.E40021)

    new_data = filter_keys(cata_meta, {
        'display': 1,
        'icon': 1
    })

    new_data['status'] = Status.editing
    new_data['updated'] = time.millisecond()

    db.catalog.update_one({'_id': ObjectId(cid)}, {'$set': new_data})
    return simple_read(cid)


def change_status(cid, action, *auth_args):
    """
    :param cid: 分类节点id
    :param action: 操作（提交，过审，驳回，上架，下架，删除等）
    :param auth_args: 鉴权参数：(signed, nonce), 即("签名的授权字符串", "临时一致性标示，需与生成签名时使用的nonce相同")
    :return:
    """

    catalog = read(cid, *auth_args)

    # 授权检查
    Passport().verify(*auth_args).operable(catalog.get('node'), 'catalog.{}'.format(action))
    # END

    cur_status = catalog.get('status')
    new_status = Status.trans(cur_status, action)

    new_data = {
        'status': new_status,
        'updated': time.millisecond()
    }

    db.catalog.update_one({'_id': ObjectId(cid)}, {'$set': new_data})

    return {'id': cid, 'status': new_status, 'old_status': cur_status}


def children(cid, *auth_args):
    c = simple_read(cid)

    # 授权检查
    # 因为授权限制操作授权本级节点，故在这里加一个'/children'，表示是读取子节点
    pp = Passport().verify(*auth_args).operable('{}/children'.format(c.get('node')), 'catalog.read')
    visible_level = pp.number(c.get('node'), 'catalog.visible_level')
    min_stat = Status.activated - visible_level
    # END

    cursor = db.catalog.find({'parent': ObjectId(cid), 'status': {'$gte': min_stat}})
    array = list()
    for item in cursor:
        item['cid'] = item.pop('_id').__str__()
        if 'parent' in item:
            item['parent'] = item['parent'].__str__()

        array.append(item)
    return array


def move(cid, cid_to, *auth_args):
    """
    把cid标示的节点移到cid_to标示的节点之下
    :param cid: 被移动节点ID
    :param cid_to: 新的父节点ID
    :param auth_args: 鉴权参数：(signed, nonce), 即("签名的授权字符串", "临时一致性标示，需与生成签名时使用的nonce相同")
    :return:
    """
    c = simple_read(cid)
    c_to = simple_read(cid_to)

    if c['parent'] == cid_to:
        raise ErrException(ERROR.E40000, extra='the same node, not need move')

    # 授权检查
    Passport().verify(*auth_args).operable(c['node'], 'catalog.remove', 'grant.remove')
    Passport().verify(*auth_args).operable(c_to['node'], 'catalog.create', 'grant.create')
    # END

    if c['status'] not in (Status.editing, Status.auditing, Status.sleeping, Status.activated):
        raise ErrException(ERROR.E40021)

    now = time.millisecond()

    name = c['node'].split('/').pop()
    node = f'{c_to["node"]}/{name}'

    if db.catalog.find_one({'node': node, 'status': {'$gte': 0}}) is not None:
        raise ErrException(ERROR.E40020)

    tmp_c = {
        'node': node,
        'parent': ObjectId(cid_to),
        'status': Status.auditing,
        'updated': now
    }

    tmp_c2o = {
        'catalog_node': node,
        'updated': now
    }

    # 还需要同步修改与此节点相关catalog2org记录，因为里面记录了节点的node值。多个地方更新需要用到事务！
    with db.start_session() as s:
        s.start_transaction()
        db.catalog2org.update_many({'catalog': ObjectId(cid)}, {'$set': tmp_c2o})
        db.catalog.update_one({'_id': ObjectId(cid)}, {'$set': tmp_c})
        s.commit_transaction()

    return simple_read(cid)
