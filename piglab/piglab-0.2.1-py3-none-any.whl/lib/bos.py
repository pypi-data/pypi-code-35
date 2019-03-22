#!/usr/bin/env python
# coding=utf-8

import os
import sys
import logging

# 从Python SDK导入BOS配置管理模块以及安全认证模块
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials
# 导入BOS相关模块
from baidubce import exception
from baidubce.services import bos
from baidubce.services.bos import canned_acl
from baidubce.services.bos.bos_client import BosClient


class Bos():
    # 设置BosClient的Host，Access Key ID和Secret Access Key
    bos_host = "bj.bcebos.com"
    # bce
    # access_key_id = "792a72e7bdc942e2b25a474dd4ce1c5f"
    # secret_access_key = "8dbb0e871d08440bb45d5f3277e72862"
    # mars
    access_key_id = "166435bd55bd4c6d973ef5518548d6b2"
    secret_access_key = "a94b08aa027e41669e56d8991f71a97b"

    def __init__(self):
        # 创建BceClientConfiguration
        config = BceClientConfiguration(credentials=BceCredentials(self.access_key_id, self.secret_access_key), endpoint=self.bos_host)

        # 新建BosClient
        self.bos_client = BosClient(config)

    def push_object(self, file_name, bucket_name='mars'):
        object_key = os.path.basename(file_name)
        return self.bos_client.put_object_from_file(bucket_name, object_key, file_name)

    def get_object(self, object_key, bucket_name='mars'):
        return self.bos_client.get_object_to_file(bucket_name, object_key, "./" + object_key)


if __name__ == '__main__':
    bos = Bos()
    file_name = '/Users/yanjingang/project/piglab/machinelearning/video/clear_video_ad/data/video/1.out.mp4'
    res = bos.push_object(file_name)
    print(res)
