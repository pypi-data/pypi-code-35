#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import string
import sys

from ..util_core.group import SS
from ..util_core.writer import GroupWriter
from ..util_core.selector import GroupSelector
from ..util_core.utils import ss_method, ColorStr

class SSFactory:
    def __init__(self):
        self.method_tuple = ss_method()

    def get_method(self):
        print ("please select shadowsocks method:")
        for index, method in enumerate(self.method_tuple):
            print ("{}.{}".format(index + 1, method))
        choice = input()
        choice = int(choice)
        if choice < 0 or choice > len(self.method_tuple):
            print("input out of range!!")
            exit(-1)
        else:
            return self.method_tuple[choice - 1]

    def get_password(self):
        random_pass = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        new_pass =input("random generate password {}, enter to use, or input customize password: ".format(ColorStr.green(random_pass)))
        if not new_pass:
            new_pass = random_pass
        return new_pass

def modify(alter_type='method'):
    # 外部传参来决定修改哪种, 默认修改method
    correct_way = ("method", "password")

    if alter_type not in correct_way:
        print("input error!")
        exit(-1)

    gs = GroupSelector('modify SS')
    group = gs.group

    if group == None:
        exit(-1)
    elif type(group.node_list[0]) != SS:
        print("\nlocal group not Shadowsocks protocol!\n")
        exit(-1)
    else:
        sm = SSFactory()
        gw = GroupWriter(group.tag, group.index)
        if alter_type == correct_way[0]:
            gw.write_ss_method(sm.get_method())
        elif alter_type == correct_way[1]:
            gw.write_ss_password(sm.get_password())
        print("modify Shadowsocks {} success!\n".format(alter_type))