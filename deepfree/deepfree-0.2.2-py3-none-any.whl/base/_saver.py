# -*- coding: utf-8 -*-
import tensorflow as tf
import os

class Saver(object):
    def __init__(self,
                 save_name,
                 sess,
                 load_phase,
                 save_model):
        self.save_name = save_name
        self.sess = sess
        self.load_phase = load_phase
        self.save_model = save_model
        self.saver = tf.train.Saver()
        
    def get_saver_str(self,phase):
        if phase == 'p': folder = 'pre_model'
        else: folder = 'ft_model'
        path = '../saver/'+ self.save_name + '/' + folder
        file = path + '/' + folder + '.ckpt'
        return folder,path,file
    
    def load_parameter(self, phase):
        folder, path, file = self.get_saver_str(phase)
        
        if phase == self.load_phase:
            print("Restore "+ folder +"...")
            if not os.path.exists(path): os.makedirs(path)
            self.saver.restore(self.sess,file)
            return True
        return False
    
    def save_parameter(self, phase):
        if self.save_model:
            folder, path, file = self.get_saver_str(phase)
            print("Save "+ folder +"...")
            if not os.path.exists(path): os.makedirs(path)
            self.saver.save(self.sess,file) 

class Tensorboard(object):
    def __init__(self,
                 save_name,
                 sess):
        self.save_name = save_name
        self.sess = sess
        # 定义 FileWriter 用于记录 merge
        write_path = '../tensorboard/'+self.save_name
        if not os.path.exists(write_path): os.makedirs(write_path)
        self.train_writer = tf.summary.FileWriter(write_path, self.sess.graph)
        
    def scalars_histogram(name,var):
        """Attach a lot of summaries to a Tensor (for TensorBoard visualization)."""
        with tf.name_scope(name):
          mean = tf.reduce_mean(var)
          stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
          # 使用tf.summary.scaler记录下var的标准差，均值
          tf.summary.scalar('stddev', stddev)
          tf.summary.scalar('mean', mean)
          # 用直方图记录参数的分布
          tf.summary.histogram('distribution', var)