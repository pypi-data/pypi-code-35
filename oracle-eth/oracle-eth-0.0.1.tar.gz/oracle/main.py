#!/usr/bin/env python
# -*- coding: utf-8 -*-

from oracle.business import ArmyEvent, import_event, OrganizationEvent
from oracle import setting
import click
import os


@click.command()
@click.option('-f', "--file", default='/etc/oracle.conf', help='指定配置文件的路径（默认: /etc/oracle.conf）')
def army(file):
    # TODO: 军队 运行的oracle程序"
    # 初始化配置信息
    setting.read_config2(file)
    print(setting.VAR)
    army = ArmyEvent()
    army.monitor_event('DIDAttributeChange')


@click.command()
@click.option('-f', "--file", default='/etc/oracle.conf', help='指定配置文件的路径（默认: /etc/oracle.conf）')
def organization(file):
    # TODO: 机构 运行的oracle程序"
    # 初始化配置信息
    setting.read_config2(file)
    print(setting.VAR)
    organization = OrganizationEvent()
    organization.monitor_event('DIDAttributeChange')


@click.command()
@click.option('-f', "--file", default='/etc/oracle.conf', help='指定配置文件的路径（默认: /etc/oracle.conf）')
def dpm(file):
    # TODO: 事务部的oracle程序"
    setting.read_config(file)


@click.command()
@click.option('-f', "--file", default='/etc/oracle.conf', help='指定配置文件的路径（默认: /etc/oracle.conf）')
def impevent(file):
    """
    导入event数据到数据库中
    :param file: 配置文件的路径
    :return:
    """
    # global PATH
    # setting.PATH = os.path.dirname(os.path.abspath(__file__))
    # 初始化配置信息
    setting.read_config2(file)
    # business.monitor_event('DIDOwnerChanged')
    import_event()


if __name__ == "__main__":
    # impevent()
    army()
