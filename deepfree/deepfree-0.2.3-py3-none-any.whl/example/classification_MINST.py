import tensorflow as tf
import numpy as np
np.random.seed(1337)  # for reproducibility

from deepfree.model.ft_model import DBN, SAE

from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets('../dataset/MNIST_data', one_hot=True)

datasets = [mnist.train.images, mnist.train.labels, mnist.test.images, mnist.test.labels]

x_dim=datasets[0].shape[1]
y_dim=datasets[1].shape[1]
p_dim=int(np.sqrt(x_dim))

# reset graph
tf.reset_default_graph()

select_method = 1

if select_method==1:
    classifier = DBN(
                 hidden_func=['sigmoid'],
                 output_func='softmax',
                 loss_func='cross_entropy',
                 struct=[x_dim, 100, 50, y_dim],
                 lr=1e-3,
                 task='classification',
                 opt='rmsp',
                 epoch=18,
                 batch_size=1280,
                 dropout_rate=0.12,
                 units_type=['gaussian','binary'],
                 pre_lr=1e-3,
                 pre_epoch=1,
                 cd_k=1)
if select_method==2:
    classifier = SAE(
                 hidden_func=['sigmoid'],
                 output_func='softmax', 
                 loss_func='cross_entropy', 
                 struct=[x_dim, 100, 50, y_dim],
                 lr=1e-3,
                 task='classification',
                 epoch=18,
                 batch_size=1280,
                 dropout_rate=0.12,
                 sub_type='ae', # ae | dae | sae
                 sub_func=['sigmoid','sigmoid'], # decoder：[sigmoid] with ‘cross_entropy’ | [linear] with ‘mse’
                 noise_type='mn', # Gaussian noise (gs) | Masking noise (mn)
                 beta=0.5, # DAE：噪声损失系数 | SAE：稀疏损失系数
                 prob=0.3, # DAE：样本该维作为噪声的概率 / SAE稀疏性参数：期望的隐层平均活跃度（在训练批次上取平均）
                 pre_lr=1e-3,
                 pre_epoch=1,
                 pre_train=True)
classifier.training(datasets = datasets)

# end sess
classifier.end_sess()