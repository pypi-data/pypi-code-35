#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : userhelp.py
@Author: donggangcj
@Date  : 2019/3/25
@Desc  : 删除DCE中用户、租户、团队、及其之间的授权关系
         数据库中删除对应的表关系
'''
import logging

from .database import User, sqlalchemy_session, Team, Tenant, Cluster
from .dce import DceClient


def _delete_user(user_id):
    """
    delete the user from t_ucs_user
    :param user_id:
    """
    with sqlalchemy_session() as session:
        user = session.query(User).filter(User.user_id == user_id).one_or_none()
        if user:
            logging.info(user)
            session.delete(user)
            session.commit()
            logging.info("USER:{} delete successfully".format(user_id))


def _delete_team(user_id):
    """
    delete the user_team from t_ucs_user_team
    :param user_id: user id from haier user center
    """
    with sqlalchemy_session() as session:
        team = session.query(Team).filter(Team.user_id == user_id).one_or_none()
        if team:
            session.delete(team)
            session.commit()
            logging.info("USER_TEAM:{} delete successfully".format(user_id))


def _delte_tenant(cluster_id, tenant_name, team_name):
    """
    delte the team_tenant from t_ucs_team_tenant
    :param cluster_id: dce host ip
    :param tenant_name: u+`team_name`
    :param team_name: user id from haier user center
    """
    with sqlalchemy_session() as session:
        tenant = session.query(Tenant).filter_by(cluster_id=cluster_id, team_name=team_name,
                                                 tenant_name=tenant_name).one_or_none()
        if tenant:
            session.delete(tenant)
            session.commit()
            logging.info(
                "TEAM_TENANT:cluster_id-{},team-{},tenant-{} delete successfully".format(cluster_id, team_name,
                                                                                         tenant_name))


def get_cluster():
    """
    get the dce clusters configuration from database
    :return:
    """
    with sqlalchemy_session() as session:
        clusters = session.query(Cluster).all()
        return clusters


def get_user_list():
    """
    Get the user  from database and dce designated user(like '2005043745')
    :rtype: object
    """
    with sqlalchemy_session() as session:
        user_list = session.query(User).all()
        users = [item.user_id for item in user_list]
        return users


# TODO Add a default parameter:delete the database users
def clean_user(user_identities=None, from_database=False):
    logging.basicConfig(level=logging.INFO)
    logging.info("======DCE USER HELPER======")

    if from_database:
        user_identities = [str(item) for item in get_user_list()]
    else:
        if not isinstance(user_identities, list):
            user_identities = user_identities.split(',')

    for user_indentity in user_identities:
        logging.info("USER INDENTITY:{}".format(user_indentity))

        logging.info('======CLEANING DCE INFORMATION======')
        for cluster in get_cluster():
            logging.info('')
            logging.info("=====CLUSTER_ID:{}".format(cluster.cluster_id))
            dceclient = DceClient(cluster.cluster_ip, cluster.cluster_key, cluster.cluster_secret,
                                  cluster_id=cluster.cluster_id)

            # print(dceclient.get_all_users())

            dceclient.remove_user(user_indentity)
            dceclient.remove_team(user_indentity)
            dceclient.remove_tenant(user_indentity)
            dceclient.remove_registry(user_indentity)

        logging.info('')
        logging.info('======CLEANING DATABASE======')
        _delete_user(user_indentity)
        _delete_team(user_indentity)
        for cluster in get_cluster():
            _delte_tenant(cluster.cluster_id, 'u' + user_indentity, user_indentity)

        logging.info('')
        logging.info("======UCS CLEANING SUCCESSFULLY======")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # clean_user(list(map(str, [2005043745])))
    clean_user(list(map(str, [2005021426])))
    # clean_user(None,from_database=True)
