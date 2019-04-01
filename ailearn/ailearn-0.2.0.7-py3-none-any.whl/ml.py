# -*- coding: utf-8 -*-
# Copyright 2018 Zhao Xingyu & An Yuexuan. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import numpy as np
import warnings


# 主成分分析
def PCA(x, feature_num=None, svd=False):
    # x：样本
    # feature_num：保留的特征数
    x = np.array(x, np.float)
    if len(x.shape) != 1 and len(x.shape) != 2:
        warnings.warn('数据维度不正确，不执行操作！')
        return None
    if len(x.shape) == 1:
        x = np.expand_dims(x, 0)
    if feature_num is None:
        feature_num = x.shape[1]
    x -= x.mean(0, keepdims=True)
    if svd:
        U, S, VT = np.linalg.svd(x)
        index_sort = np.argsort(S)  # 对奇异值进行排序
        index = index_sort[-1:-(feature_num + 1):-1]
        return x.dot(VT.transpose()[:, index])  # 乘上最大的feature_num个特征组成的特征向量
    else:
        eigval, eigvec = np.linalg.eig(x.transpose().dot(x) / x.shape[0])
        index_sort = np.argsort(eigval)  # 对特征值进行排序
        index = index_sort[-1:-(feature_num + 1):-1]
        return x.dot(eigvec[:, index])  # 乘上最大的feature_num个特征组成的特征向量
