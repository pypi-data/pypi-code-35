from __future__ import division
from __future__ import print_function

import keras

from keras.applications import resnet50, densenet, inception_v3, inception_resnet_v2, mobilenetv2, nasnet, xception
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import multi_gpu_model
import numpy as np
import cv2
from math import ceil
import os
import json
from collections import OrderedDict

from ....lib.general_lib import reverse_dict, DataGenerator
from ....lib.image_lib import directory_images_to_arrays
from ....lib.image_proccessing.image_classification.saving_lib import load_model, save_model
from ....lib.custom_callback import Callback_Image_Classification

from ...application import Application



class Image_Classification(Application):
    def __init__(self, model_path = None, model_type = 'densenet121'):
        super().__init__()
        if type(model_path) != type(None):
            self.load(model_path)
        else:
            self.model_type = model_type
    

    def prepare_train_data(self, get_image_from = 'directory', data_path = None, data_array = None, target_array = None, optimizer = 'nadam', metrics = ['accuracy']):
        self.get_image_from = get_image_from
        self.data_path = data_path
        if hasattr(self, 'model'):
            if self.get_image_from == 'argument':
                return self.reshape_data(data_array), target_array
            else:
                return
        
        if self.get_image_from == 'argument':
            if type(data_array) == type(None) or type(target_array) == type(None):
                raise TypeError('you should prepare arrays to initialize model')
            else:
                unique_classes = np.lib.arraysetops.unique(target_array)
                class_indices = self.create_class_indices(unique_classes)
                self.create_and_compile_model(class_indices, optimizer, metrics)
                return self.reshape_data(data_array), target_array
        else:
            if self.get_image_from != 'directory':
                raise ValueError("value of get_image_from should be either 'directory' or 'argument'.")
            else:
                class_indices = {}
                for i, c in enumerate(sorted(os.listdir(data_path))):
                    if os.path.isdir(os.path.join(data_path, c)):
                        class_indices[c] = i
                self.create_and_compile_model(class_indices, optimizer, metrics)
                return


    def compile_model(self, optimizer, loss, metrics=['accuracy']):
        self.model.compile(optimizer, loss=loss, metrics=metrics)


    def create_and_compile_model(self, class_indices = None, optimizer = 'nadam', metrics = ['accuracy']):
        num_classes = len(class_indices)
        if self.model_type == 'densenet121':
            self.model = densenet.DenseNet121( weights=None, classes=num_classes )
        elif self.model_type == 'inception_v3':
            self.model = inception_v3.InceptionV3( weights=None, classes=num_classes )
        elif self.model_type == 'inception_resnet_v2':
            self.model = inception_v3.InceptionV3( weights=None, classes=num_classes )
        elif self.model_type == 'mobilenet_v2':
            self.model = mobilenetv2.MobileNetV2( weights=None, classes=num_classes )
        elif self.model_type == 'nasnet_large':
            self.model = nasnet.NASNetLarge( weights=None, classes=num_classes )
        elif self.model_type == 'nasnet_mobile':
            self.model = nasnet.NASNetMobile( weights=None, classes=num_classes )
        elif self.model_type == 'xception':
            self.model = xception.Xception( weights=None, classes=num_classes )
        elif self.model_type == 'resnet50' :
            self.model = resnet50.ResNet50( weights=None, classes=num_classes)
        try:
            self.model = multi_gpu_model(self.model, gpus = self.gpu_num, cpu_relocation=True)
        except ValueError:
            self.model = self.model        
        self.model.class_indices = class_indices
        self.compile_model(optimizer = optimizer, loss = keras.losses.categorical_crossentropy, metrics = metrics)


    def train(self,
            x_train = None,
            target_array = None,
            image_data_generator = None,
            batch_size = 32,
            epochs = 1,
            verbose = 0,
            callbacks = None,
            shuffle = True
        ):

        if type(image_data_generator) == type(None):
            if self.get_image_from == 'directory':
                train_datagen = self.create_image_data_generator(rescale = 1./255)
            else:
                train_datagen = self.create_image_data_generator()
        else:
            train_datagen = image_data_generator
        if self.get_image_from == 'directory':
            train_generator = train_datagen.flow_from_directory(self.data_path, target_size = self.model.input_shape[1:3], class_mode = 'categorical', batch_size = batch_size)
            num_dataset = 0
            for root, dirs, files in os.walk(self.data_path):
                for basename in files:
                    file_extension = basename.split('.')[-1]
                    if file_extension in ('jpg', 'jpeg', 'png', 'bmp', 'ppm', 'tif', 'tiff'):
                        num_dataset += 1
            steps_per_epoch = ceil(num_dataset / batch_size)

            if self.deepblock_log == True:
                callbacks = [Callback_Image_Classification(total_step = steps_per_epoch, total_epoch = epochs)]
            else :
                callbacks = []    
            self.model.fit_generator(train_generator, steps_per_epoch=steps_per_epoch, epochs=epochs, verbose=verbose, callbacks=callbacks, shuffle=shuffle)
        elif self.get_image_from == 'argument':
            y_train = self.prepare_y( target_array, reverse_dict(self.model.class_indices), len(self.model.class_indices) )
            train_generator = train_datagen.flow(x_train, y_train, batch_size = batch_size)
            num_dataset = x_train.shape[0]
            steps_per_epoch = ceil(num_dataset / batch_size)
            self.model.fit_generator(train_generator, steps_per_epoch=steps_per_epoch, epochs=epochs, verbose=verbose, callbacks=callbacks, shuffle=shuffle)


    def load(self, model_path = None):
        try:
            self.model = load_model(model_path)
        except Exception as e:
            print("Model loading failed")
            print(e)
            raise e


    def save(self, model_path):
        try:
            if type(self.model) == type(None):
                raise TypeError('You should create a model before saving it')
            save_model(self.model, model_path, class_indices = self.model.class_indices)
        except Exception as e:
            raise e


    def predict(self, data_array = None, data_path = None, predict_classes = True, batch_size = 16, verbose = 0, steps = None):
        try:
            if type(data_path) == type(None):
                raise TypeError('You sholud give a proper data path')

            output_dictionary = reverse_dict(self.model.class_indices)

            pair_dict = OrderedDict()
            # check data_path is file or folder
            if os.path.isdir(data_path):
                datagen = DataGenerator()
                
                predict_data_generator = datagen.flow_one_directory(
                    directory_path = data_path,
                    shuffle = False,
                    batch_size = batch_size,
                    image_shape = self.model.input_shape[1:3]
                )

                nb_files = len(predict_data_generator.image_filenames)
                probs = self.model.predict_generator(predict_data_generator, steps=ceil(nb_files/batch_size))
                predicted_classes = probs.argmax(axis=-1)

                predicted_order_filenames = predict_data_generator.predict_order_filenames

                for i in range(len(predicted_classes)):
                    pair_dict[predicted_order_filenames[i]] = output_dictionary[predicted_classes[i]]
                return json.dumps(pair_dict, ensure_ascii=False)
            else:
                _, only_file_name = os.path.split(data_path)
                img_to_predict = cv2.imread(data_path)
                img_array = np.expand_dims(img_to_predict, axis=0)
                reshaped_array = self.reshape_data(img_array)
                probs = self.model.predict(reshaped_array, batch_size=batch_size, verbose=verbose, steps=steps)
                predicted_class = probs.argmax(axis=-1)
                pair_dict[only_file_name] = output_dictionary[predict_classes]
                return json.dumps(pair_dict, ensure_ascii=False)
        except Exception as e:
            raise e

    
    # You have to give data_path exactly same as train dataset
    def evaluate(self, data_path = None):
        try:
            total_nb = 0
            total_right_predict = 0
            class_folders = os.listdir(data_path)
            for i in range(len(class_folders)):
                right_predict = 0
                one_class_folder_path = os.path.join(data_path, class_folders[i])
                answer = class_folders[i]
                predict_list = self.predict(data_path = one_class_folder_path)
                for j in range(len(predict_list)):
                    if predict_list[j] == answer:
                        right_predict = right_predict + 1
                        total_right_predict = total_right_predict + 1

                print(answer + ":" + str(right_predict/len(predict_list)))

                total_nb = total_nb + len(predict_list)
            print("Total predict evaluation result : " + str(total_right_predict/total_nb))
        except Exception as e:
            raise e


    def check_one_image_in_folder(self, data_path = None):
        try:
            if not os.path.isdir(data_path):
                raise FileNotFoundError(data_path + " does not exist")
            files = os.listdir(data_path)
            evaulate_file = files[0]
            predicted_data = self.predict( data_path = os.path.join(data_path, evaulate_file) )
            return predicted_data.item(0)
        except Exception as e :
            raise e


    def create_class_indices(self, unique_classes):
        class_indices = dict()
        for i in range(unique_classes.shape[0]):
            class_indices[unique_classes[i]] = i
        return class_indices


    def create_image_data_generator(self, featurewise_center=False,  # set input mean to 0 over the dataset
            samplewise_center=False,  # set each sample mean to 0
            featurewise_std_normalization=False,  # divide inputs by std of the dataset
            samplewise_std_normalization=False,  # divide each input by its std
            zca_whitening=False,  # apply ZCA whitening
            zca_epsilon=1e-06,  # epsilon for ZCA whitening            
            rotation_range=0.,  # randomly rotate images in the range (degrees, 0 to 180)
            width_shift_range=0.,  # randomly shift images horizontally (fraction of total width)
            height_shift_range=0.,  # randomly shift images vertically (fraction of total height)
            brightness_range=None,
            shear_range=0.,  # set range for random shear(Shear angle in counter-clockwise direction in degrees)
            zoom_range=0.,  # set range for random zoom. If a float, `[lower, upper] = [1-zoom_range, 1+zoom_range]`.
            channel_shift_range=0.,  # set range for random channel shifts
            fill_mode='nearest',  # One of {"constant", "nearest", "reflect" or "wrap"}
            cval=0.,  # value used for fill_mode = "constant"
            horizontal_flip=True,  # randomly flip images
            vertical_flip=False,  # randomly flip images
            rescale=None,  # set rescaling factor (applied before any other transformation)
            preprocessing_function=None,  # set function that will be applied on each input
            data_format="channels_last",  # either "channels_first" or "channels_last"
            validation_split=0.0  # fraction of images reserved for validation (strictly between 0 and 1)
        ):
            return ImageDataGenerator(featurewise_center,
                samplewise_center,
                featurewise_std_normalization,
                samplewise_std_normalization,
                zca_whitening,
                zca_epsilon,
                rotation_range,
                width_shift_range,
                height_shift_range,
                brightness_range,
                shear_range,
                zoom_range,
                channel_shift_range,
                fill_mode,
                cval,
                horizontal_flip,
                vertical_flip,
                rescale,
                preprocessing_function,
                data_format,
                validation_split)


    def prepare_y(self, target_array, class_indices, num_classes):
        """Prepares y for a keras model.(ex. y_train)
        
        Arguments:
            target_array {ndarray} -- ndarray. Appropriate outputs of input data.
            class_indices {dict} -- A dictionary of classes to targets.
            num_classes {int} -- A number of the entire classes.
        
        Returns:
            [ndarray] -- A binary matrix representation of the input.
        """
        y_list = list()
        for i in range(target_array.shape[0]):
            label_class = class_indices[target_array[i]]
            y_list.append(label_class)        
        y = keras.utils.to_categorical(np.asarray(y_list), num_classes)
        return y


    def reshape_data(self, data_array, cv_interpolation = cv2.INTER_LINEAR):
        """Changes an array of images to fit with model's input.
        Note that this method casts and rescales data to a range of [0, 1].
        
        Arguments:
            data_array {ndarray} -- An array of images.
        
        Keyword Arguments:
            cv_interpolation {int} -- cv2 interpolation. (default: {cv2.INTER_LINEAR})

        Returns:
            [ndarray] -- Reshaped data array.
        """
        if data_array.shape[1:] != self.model.input_shape:
            reshaped_list = list()
            for i in range(data_array.shape[0]):
                resized_img = cv2.resize(data_array[i], (self.model.input_shape[1], self.model.input_shape[2]), interpolation = cv_interpolation)
                reshaped_list.append(resized_img)
            data_array = np.asarray(reshaped_list)
            reshaped_list = [] # empty list after use
        data_array = data_array.astype('float32')
        data_array /= 255
        return data_array

