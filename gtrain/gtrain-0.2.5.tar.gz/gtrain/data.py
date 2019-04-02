import math

import numpy as np
from abc import ABC

class Data(ABC):
    def set_placeholders(self, pl_list):
        self.placeholders = pl_list

    def get_next_batch(self):
        pass

    def accumulate_grad(self):
        pass

    def accumulate_dev(self):
        return self.accumulate_grad()

    def get_next_dev_batch(self):
        pass

    def train_ended(self):
        pass

def generate_test_data(num_of_train_samples = 1000, num_of_validation_samples=100):
        data_tr = np.random.rand(num_of_train_samples,2)
        data_val = np.random.rand(num_of_validation_samples,2)
        l_tr = np.zeros([num_of_train_samples,3])
        l_val = np.zeros([num_of_validation_samples,3])

        def sample_class(sample) :
            if (sample[0]*sample[0]+sample[1]*sample[1])<0.0:
                return 0
            else :
                if sample[1]>0.5:
                    return 1
                else:
                    return 2

        for i in range(len(l_tr)) :
            l_tr[i][sample_class(data_tr[i])]=1
        for i in range(len(l_val)) :
            l_val[i][sample_class(data_val[i])]=1
        return data_tr,l_tr,data_val,l_val


class AllData(Data):
    #example of child of Data class

    def __init__(self, train_input, train_target, test_input, test_target):
        self.train_input = train_input
        self.train_target = train_target
        self.test_input = test_input
        self.test_target = test_target
        self.counter = False
        
    def set_placeholders(self,pl_list):
        self.ph_x = pl_list[0]
        self.ph_y = pl_list[1]

    def get_next_batch(self):
        return {self.ph_x: self.train_input, self.ph_y: self.train_target }
    
    def accumulate_grad(self):
        #self.counter = not self.counter
        return False

    def accumulate_dev(self):
        return False

    def get_next_dev_batch(self):
        return {self.ph_x: self.test_input, self.ph_y: self.test_target }
    
    def train_ended(self):
        pass


class BatchedData(Data):


    def __init__(self, train_input, train_target, test_input, test_target, batch_size=32):
        self.train_input = train_input
        self.train_target = train_target
        self.test_input = test_input
        self.test_target = test_target
        self.batch_size = batch_size
        self.batch_num = math.ceil(train_input.shape[0]/batch_size)
        self.counter = 0
        self.start_index = 0
        self.end_index = batch_size-1

    def set_placeholders(self, pl_list):
        self.ph_x = pl_list[0]
        self.ph_y = pl_list[1]

    def get_next_batch(self):
        feet_dict = {
            self.ph_x: self.train_input[self.start_index:self.end_index],
            self.ph_y: self.train_target[self.start_index:self.end_index]}
        if self.end_index == self.train_input.shape[0]-1:
            self.start_index = 0
            self.end_index = self.batch_size - 1
        else:
            if self.end_index + self.batch_size >=  self.train_input.shape[0]:
                self.end_index = self.train_input.shape[0]-1
            else:
                self.end_index += self.batch_size
            self.start_index += self.batch_size
        return feet_dict

    def accumulate_grad(self):
        return False
        self.counter += 1
        if self.counter % self.batch_num == 0:
            self.counter = 0
            return False
        else:
            return True

    def accumulate_dev(self):
        return False

    def get_next_dev_batch(self):
        return {self.ph_x: self.test_input, self.ph_y: self.test_target}

    def train_ended(self):
        pass