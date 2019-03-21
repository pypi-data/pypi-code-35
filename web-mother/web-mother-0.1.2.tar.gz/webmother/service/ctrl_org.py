# coding:utf-8

from webmother.db import mongo as db
from tweb.json_util import filter_keys
from tweb.error_exception import ErrException, ERROR
from tweb import time
from bson.objectid import ObjectId
from bson.errors import InvalidId
from webmother.service.identity import Identity
import re
import base64
from webmother.service import ctrl_catalog
from webmother.service.passport import Passport

internal_org_name = ['vip']


# 组织节点状态以及状态迁移定义
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


def create(oid, org_meta, *auth_args):
    """
    向oid节点中添加org_meta描述的子节点
    """
    o = simple_read(oid)

    # 授权检查
    Identity().verify(*auth_args).operable(o.get('node'), 'org.create')
    # END

    name = org_meta['name'].lower()
    if name in internal_org_name:
        raise ErrException(ERROR.E40000, extra='org name should not be %s' % internal_org_name)

    return simple_create(oid, org_meta)


def simple_create(oid, org_meta):
    o = simple_read(oid)

    name = org_meta.pop('name').lower()
    if not re.match(r'^[\w]{0,19}$', name):
        raise ErrException(ERROR.E40000, extra='name should be letter, number, _, and beginning with letter')

    org_meta['node'] = '{}/{}'.format(o['node'], name)
    org_meta['parent'] = ObjectId(oid)

    if db.org.find_one({'node': org_meta['node'], 'status': {'$gte': 0}}) is not None:
        raise ErrException(ERROR.E40020)

    org_meta['status'] = Status.editing
    now = time.millisecond()
    org_meta['created'] = now
    org_meta['updated'] = now

    result = db.org.insert_one(org_meta)
    return simple_read(result.inserted_id)


def read(oid, *auth_args):
    o = simple_read(oid)

    # 授权检查
    Identity().verify(*auth_args).operable(o.get('node'), 'org.read')
    # END

    return o


def simple_read(oid, raw=False):
    try:
        oid_obj = ObjectId(oid)
    except InvalidId:
        raise ErrException(ERROR.E40000, extra='wrong org id')

    o = db.org.find_one({'_id': oid_obj, 'status': {'$gte': 0}})
    if o is None:
        raise ErrException(ERROR.E40400, extra=f'the org({oid}) not existed')

    if not raw:
        o['oid'] = o.pop('_id').__str__()
        if 'parent' in o:
            o['parent'] = o['parent'].__str__()

    return o


def read_with_node(node, raw=False):
    o = db.org.find_one({'node': node, 'status': {'$gte': 0}})
    if o is None:
        return None

    if not raw:
        o['oid'] = o.pop('_id').__str__()
        if 'parent' in o:
            o['parent'] = o['parent'].__str__()

    return o


def read_with_appid(appid, raw=False):
    o = db.org.find_one({'appid': appid, 'status': {'$gte': 0}})
    if o is None:
        return None

    if not raw:
        o['oid'] = o.pop('_id').__str__()
        if 'parent' in o:
            o['parent'] = o['parent'].__str__()

    return o


def update(oid, org_meta, *auth_args):
    """
    :param oid: 组织节点id
    :param org_meta: 组织信息
    :param auth_args: 鉴权参数：(signed, nonce), 即("签名的授权字符串", "临时一致性标示，需与生成签名时使用的nonce相同")
    :return:
    """
    o = simple_read(oid)

    # 授权检查
    Identity().verify(*auth_args).operable(o.get('node'), 'org.update')
    # END

    if o['status'] not in (Status.editing, Status.auditing, Status.sleeping, Status.activated):
        raise ErrException(ERROR.E40021)

    new_data = filter_keys(org_meta, {
        'display': 1,
        'icon': 1
    })

    new_data['status'] = Status.editing
    new_data['updated'] = time.millisecond()

    db.org.update_one({'_id': ObjectId(oid)}, {'$set': new_data})
    return simple_read(oid)


def change_status(oid, action, *auth_args):
    """
    :param oid: 组织节点id
    :param action: 操作（提交，过审，驳回，激活，去激活，删除等）
    :param auth_args: 鉴权参数：(signed, nonce), 即("签名的授权字符串", "临时一致性标示，需与生成签名时使用的nonce相同")
    :return:
    """
    o = simple_read(oid)

    # 授权检查
    Identity().verify(*auth_args).operable(o.get('node'), 'org.{}'.format(action))
    # END

    cur_status = o.get('status')
    new_status = Status.trans(cur_status, action)

    new_data = {
        'status': new_status,
        'updated': time.millisecond()
    }

    db.org.update_one({'_id': ObjectId(oid)}, {'$set': new_data})

    return {'id': oid, 'status': new_status, 'old_status': cur_status}


def children(oid, *auth_args):
    o = simple_read(oid)

    # 授权检查
    # 因为授权限制操作授权本级节点，故在这里加一个'/children'，表示是读取子节点
    idt = Identity().verify(*auth_args).operable('{}/children'.format(o.get('node')), 'org.read')
    visible_level = idt.number(o.get('node'), 'org.visible_level')
    min_stat = Status.activated - visible_level
    # END

    cursor = db.org.find({'parent': ObjectId(oid), 'status': {'$gte': min_stat}})
    array = list()
    for item in cursor:
        item['oid'] = item.pop('_id').__str__()
        if 'parent' in item:
            item['parent'] = item['parent'].__str__()

        array.append(item)
    return array


def move(oid, oid_to, *auth_args):
    """
    把oid标示的节点移到oid_to标示的节点之下
    :param oid: 被移动节点ID
    :param oid_to: 新的父节点ID
    :param auth_args: 鉴权参数：(signed, nonce), 即("签名的授权字符串", "临时一致性标示，需与生成签名时使用的nonce相同")
    :return:
    """
    o = simple_read(oid, raw=True)
    o_to = simple_read(oid_to, raw=True)

    if o['parent'] == oid_to:
        raise ErrException(ERROR.E40000, extra='the same node, not need move')

    # 授权检查
    Identity().verify(*auth_args).operable(o['node'], 'org.remove', 'member.remove')
    Identity().verify(*auth_args).operable(o_to['node'], 'org.create', 'member.create')
    # END

    if o['status'] not in (Status.editing, Status.auditing, Status.sleeping, Status.activated):
        raise ErrException(ERROR.E40021)

    now = time.millisecond()

    name = o['node'].split('/').pop()
    node = f'{o_to["node"]}/{name}'

    if db.org.find_one({'node': node, 'status': {'$gte': 0}}) is not None:
        raise ErrException(ERROR.E40020)

    tmp_o = {
        'node': node,
        'parent': ObjectId(oid_to),
        'status': Status.auditing,
        'updated': now
    }

    tmp_o2u = {
        'org_node': node,
        'updated': now
    }

    # 还需要同步修改与此节点相关org2user记录，因为里面记录了节点的node值。多个地方更新需要用到事务！
    with db.start_session() as s:
        s.start_transaction()
        db.org2user.update_many({'org': ObjectId(oid)}, {'$set': tmp_o2u})
        db.org.update_one({'_id': ObjectId(oid)}, {'$set': tmp_o})
        s.commit_transaction()

    return simple_read(oid)


def our_passports(oid, *auth_args):
    """
    获取组织拥有授权的分类节点列表(需有该组织的会员资格)
    :param oid: 组织ID
    :param auth_args: 鉴权参数：(signed, nonce), 即("签名的授权字符串", "临时一致性标示，需与生成签名时使用的nonce相同")
    :return:
    """

    nonce = auth_args[1]

    o = simple_read(oid)

    # 授权检查, 被查询组织必须是身份认证的组织
    idt = Identity().verify(*auth_args)
    if idt.node != o['node']:
        raise ErrException(ERROR.E40306)
    # END

    cursor = db.catalog2org.find({'org': ObjectId(oid)}, {'_id': 0, 'org': 0})

    array = list()
    for item in cursor:
        pp = Passport().parse(item['passport'])
        item['signed_passport'] = pp.signed(item['catalog_node'], oid, nonce)
        item['passport'] = pp.json

        item['catalog'] = ctrl_catalog.simple_read(item['catalog'])

        array.append(item)

    return array


def app_activate(oid, *auth_args):
    o = simple_read(oid)

    # 授权检查
    Identity().verify(*auth_args).operable(o.get('node'), 'app.create')
    # END

    if o['status'] not in (Status.editing, Status.auditing, Status.sleeping, Status.activated):
        raise ErrException(ERROR.E40021)

    if o.get('appid') is None:
        appid = str(base64.b32encode(ObjectId(o['oid']).binary), encoding="utf8")[0:20]
        new_data = {
            'appid': appid,
            'status': Status.editing,
            'updated': time.millisecond()
        }

        db.org.update_one({'_id': ObjectId(oid)}, {'$set': new_data})

    return simple_read(oid)


def appid_deactivate(oid, *auth_args):
    o = simple_read(oid)

    # 授权检查
    idt = Identity().verify(*auth_args).operable(o.get('node'), 'app.remove')
    # END

    # 不能移除自己当前的应用
    if idt.node == o['node']:
        raise ErrException(ERROR.E40300, extra='can not deactivate yourself app')

    if o['status'] not in (Status.editing, Status.auditing, Status.sleeping, Status.activated):
        raise ErrException(ERROR.E40021)

    if o.get('appid') is not None:
        db.org.update_one({'_id': ObjectId(oid)}, {'$unset': {'appid': ''}})

    return simple_read(oid)


def vip_create(appid, level, display, *auth_args):
    """
    在组织下创建客户VIP组，用以管理客户。
    客户可以自主加入最低级VIP组，然后客户升级，即从低级别组中移动到高级别VIP组中，由应用系统根据一定的策略进行升级移动
    :param appid: 组织的应用ID
    :param level: VIP组的级别，取值0～100，只有level为0的VIP组才支持客户自主加入
    :param display: 会员组显示名称对象（含多语言），如{'zh': "普通会员"，'en': "normal"}等
    :param auth_args: 操作者的鉴权信息
    :return:
    """

    o = read_with_appid(appid)
    if o is None:
        raise ErrException(ERROR.E40400, extra='invalid appid %s' % appid)

    # 授权检查
    idt = Identity().verify(*auth_args)
    idt.operable(o.get('node'), 'org.create')
    # END

    with db.start_session() as s:
        s.start_transaction()
        # begin
        # 首先创建会员管理组
        vm_o = read_with_node('{}/vip'.format(o['node']))
        if vm_o is None:
            vm_o = simple_create(o['oid'], {
                'name': 'vip',
                'display': {
                    'zh': '会员管理',
                    'en': 'Member Manage'
                }
            })

        # 然后会员管理组下创建会员组
        vip_o = read_with_node('{}/vip/{}'.format(o['node'], level))
        if vip_o is not None:
            raise ErrException(ERROR.E40020, extra='existed about the VIP of level %s' % level)

        dis = dict()
        if 'zh' in display:
            dis['zh'] = display['zh']
        if 'en' in display:
            dis['en'] = display['en']
        else:
            dis['en'] = 'vip{}'.format(level)

        vip_o = simple_create(vm_o['oid'], {
            'name': '{}'.format(level),
            'display': dis
        })
        s.commit_transaction()
        # end

        return vip_o


def vip_query(appid, *auth_args):
    o = read_with_appid(appid)
    if o is None:
        raise ErrException(ERROR.E40400, extra='invalid appid %s' % appid)

    vip_o = read_with_node('{}/vip'.format(o['node']))
    if vip_o is None:
        raise ErrException(ERROR.E40400, extra='no vip org about appid %s' % appid)

    return children(vip_o['oid'], *auth_args)
