import keras
import numpy as np
import os
import cv2
"""This module is a custom module designed for general use in the Omnis project.
"""

class DataGenerator(keras.utils.Sequence):
    def __init__(self, image_filenames = None, labels=None, batch_size=None, image_shape=None, shuffle = False):
        self.image_filenames, self.labels = image_filenames, labels
        self.batch_size = batch_size
        self.image_shape = image_shape
        self.shuffle = shuffle
        self.predict_order_filenames = []

    def __len__(self):
        return int(np.ceil(len(self.image_filenames) / float(self.batch_size)))

    def __getitem__(self, idx):
        batch_x = self.image_filenames[idx * self.batch_size:(idx + 1) * self.batch_size]

        x = []
        for filename in batch_x:
            _, only_file_name = os.path.split(filename)
            self.predict_order_filenames.append(only_file_name)
            img = cv2.imread(filename)
            test_data = np.expand_dims(img, axis=0)
            resized_img = cv2.resize(test_data[0], self.image_shape)
            x.append(resized_img)
        
        data_array = np.asarray(x)
        data_array = data_array.astype('float32')
        data_array /= 255
        return data_array


    def flow_one_directory(self, directory_path, shuffle = False, batch_size = 1, image_shape = None):
        filelist = os.listdir(directory_path)
        for i in range(len(filelist)):
            if i==0:
                self.image_filenames = [directory_path + '/' + filelist[i]]
            else :
                self.image_filenames.append(directory_path + '/' + filelist[i])
        self.batch_size = batch_size
        self.image_shape = image_shape
        self.shuffle = shuffle
        
        return self


def reverse_dict(input_dict):
    """This function returns a dictionary with input_dict's key, value is reversed.
    
    Arguments:
        input_dict {dict} -- Dictionary to reverse.
    
    Returns:
        [dict] -- Reversed dictionary.
    """
    reversed_dict = {}
    key_list = list(input_dict.keys())
    for index, val in enumerate( list(input_dict.values()) ):
        reversed_dict[val] = key_list[index]
    return reversed_dict