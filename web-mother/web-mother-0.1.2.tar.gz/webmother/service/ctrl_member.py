# coding:utf-8

from webmother.db import mongo as db
from tweb.error_exception import ErrException, ERROR
from tweb import time
from bson.objectid import ObjectId
from webmother.service.identity import Identity
from webmother.service import ctrl_org

from ucenter.services import ctrl_user


def get_identity_tpl(oid, *auth_args):
    o = ctrl_org.read(oid, *auth_args)

    # 授权检查
    Identity().verify(*auth_args).operable(o.get('node'), 'member.create')
    # END

    return Identity().json


def member_create(oid, indicator, identity_json, *auth_args):
    """
    向组织中添加用户
    :param oid: 组织ID
    :param indicator: 用户标示，可以是uid, 登录名，email, 手机号
    :param identity_json: 授权信息对象
    :param auth_args: 鉴权参数：(signed, nonce), 即("签名的授权字符串", "临时一致性标示，需与生成签名时使用的nonce相同")
    :return:
    """
    u = ctrl_user.get(indicator)
    if u is None:
        raise ErrException(ERROR.E40000, extra='invalid user [%s]' % indicator)

    uid = u['id']
    user = {
        'uid': ObjectId(uid),
        'name': u.get('name'),
        'nickname': u.get('nickname'),
        'email': u.get('email'),
        'mobile': u.get('mobile'),
        'icon': u.get('icon')
    }

    o = ctrl_org.simple_read(oid)

    # 授权检查
    idt = Identity().verify(*auth_args).operable(o.get('node'), 'member.create')
    # END

    node = o['node']
    cursor = db.org2user.find({'user.uid': ObjectId(uid)}, {'user': 0})
    for item in cursor:
        other = item['org_node']
        # 如果已经加入，则无需再加入
        if node == other:
            raise ErrException(ERROR.E40020, extra=f'user({uid}) have been in org({other})')

    now = time.millisecond()
    db.org2user.insert_one({
        "org": ObjectId(oid),
        "org_node": node,
        "identity": Identity().update(node, uid, identity_json, idt).text,
        "member_type": 0,
        "user": user,
        "created": now,
        "updated": now
    })

    return simple_member_read(oid, uid)


def member_read(oid, uid, *auth_args):
    o = ctrl_org.read(oid, *auth_args)

    # 授权检查
    Identity().verify(*auth_args).operable(o.get('node'), 'member.read')
    # END

    return simple_member_read(oid, uid)


def simple_member_read(oid, uid):
    # 首先从UCenter更新最新的用户信息
    u = ctrl_user.get(uid)
    if u is None:
        raise ErrException(ERROR.E40000, extra='invalid user [%s]' % indicator)

    user = {
        'uid': ObjectId(uid),
        'name': u.get('name'),
        'nickname': u.get('nickname'),
        'email': u.get('email'),
        'mobile': u.get('mobile'),
        'icon': u.get('icon')
    }

    # 读取会员信息
    o2u = db.org2user.find_one({'org': ObjectId(oid), 'user.uid': ObjectId(uid)}, {'org': 0})
    if o2u is None:
        raise ErrException(ERROR.E40400)

    # 如果UCenter中的信息更新，则同步更新到会员系统
    if user != o2u['user']:
        db.org2user.update_one({'org': ObjectId(oid), 'user.uid': ObjectId(uid)}, {'$set': {'user': user}})
        o2u['user'] = user

    o2u['open_id'] = o2u.pop('_id').__str__()
    o2u['user']['uid'] = o2u['user']['uid'].__str__()
    o2u['identity'] = Identity().parse(o2u['identity']).json

    return o2u


def member_update(oid, uid, identity_json, *auth_args):
    o = ctrl_org.read(oid, *auth_args)

    # 授权检查
    idt = Identity().verify(*auth_args).operable(o.get('node'), 'member.update')
    # END

    o2u = db.org2user.find_one({'org': ObjectId(oid), 'user.uid': ObjectId(uid)})
    if o2u is None:
        raise ErrException(ERROR.E40400)

    temp = dict()
    temp['identity'] = Identity().parse(o2u.get('identity')).update(o['node'], uid, identity_json, idt).text
    temp['updated'] = time.millisecond()
    db.org2user.update_one({'_id': o2u['_id']}, {'$set': temp})

    return simple_member_read(oid, uid)


def member_remove(oid, uid, *auth_args):
    """
    从组织中移除用户
    :param oid: 组织ID
    :param uid: 用户ID
    :param auth_args: 鉴权参数：(signed, nonce), 即("签名的授权字符串", "临时一致性标示，需与生成签名时使用的nonce相同")
    :return:
    """
    o = ctrl_org.simple_read(oid)

    # 授权检查
    Identity().verify(*auth_args).operable(o.get('node'), 'member.remove')
    # END

    # 使已签名的授权无效
    Identity.invalidate_signed(o.get('node'), uid)

    db.org2user.delete_one({'org': ObjectId(oid), 'user.uid': ObjectId(uid)})

    return {}


def members_query(oid, *auth_args):
    o = ctrl_org.simple_read(oid)

    # 授权检查
    Identity().verify(*auth_args).operable(o.get('node'), 'member.read')
    # END

    cursor = db.org2user.find({'org': ObjectId(oid)}, {'org': 0})

    array = list()
    for item in cursor:
        item['open_id'] = item.pop('_id').__str__()
        item['user']['uid'] = item['user']['uid'].__str__()
        item['identity'] = Identity().parse(item['identity']).json
        array.append(item)

    return array
