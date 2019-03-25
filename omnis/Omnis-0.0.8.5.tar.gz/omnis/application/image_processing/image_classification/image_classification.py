from __future__ import division
from __future__ import print_function

import keras

from keras.applications import resnet50, densenet, inception_v3, inception_resnet_v2, mobilenetv2, nasnet, xception
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import multi_gpu_model
import numpy
from glob import glob
import cv2
from math import ceil
import os

from ....lib.general_lib import reverse_dict
from ....lib.image_lib import directory_images_to_arrays
from ....lib.image_proccessing.image_classification.saving_lib import load_model, save_model

from ...application import Application


class Image_Classification(Application):
    def __init__(self, input_shape = None, model_path = None, model_type = None, class_list_path = None):
        super().__init__()

        self.model_type = model_type
        if type(model_path) != type(None):
            self.load(model_path, class_list_path)
        if type(input_shape) != type(None):            
            self.input_shape = input_shape
    

    def prepare_train_data(self, get_image_from = 'directory', data_path = None, data_array = None, target_array = None):
        self.get_image_from = get_image_from
        self.data_path = data_path
        if self.get_image_from == 'argument':
            if type(data_array) == type(None) or type(target_array) == type(None):
                raise TypeError('you should prepare arrays to initialize model')
            else:
                unique_classes = numpy.lib.arraysetops.unique(target_array)
                self.class_indices = self.create_class_indices(unique_classes)
                self.num_classes = len(self.class_indices)
                self.create_model()
                return self.reshape_data(data_array), target_array
        else:
            if self.get_image_from != 'directory':
                raise ValueError("value of get_image_from should be either 'directory' or 'argument'.")
            else:
                self.class_indices = {}
                for i, c in enumerate(sorted(os.listdir(data_path))):
                    if os.path.isdir(data_path + '/' + c):
                        self.class_indices[c] = i
                self.num_classes = len(self.class_indices)
                self.create_model()
                return None, None


    def train(self,
            x_train = None,
            target_array = None,
            optimizer = 'nadam',
            metrics = ['accuracy'],
            image_data_generator = None,
            batch_size = 32,
            epochs = 1,
            verbose = 1,
            callbacks = None,
            shuffle = True,
            use_fit_generator = True
        ):
        if use_fit_generator == False:
            if self.get_image_from == 'directory':
                x_train, target_array = directory_images_to_arrays(self.data_path, self.input_shape[:2])
            self.compile_model(optimizer = optimizer, loss = keras.losses.categorical_crossentropy, metrics = metrics)
            y_train = self.prepare_y(target_array, reverse_dict(self.model.class_indices), self.num_classes)
            self.model.fit(x_train, y_train, batch_size = batch_size, steps_per_epoch=None, epochs=epochs, verbose=verbose, callbacks=callbacks, shuffle=shuffle)
        else:
            if type(image_data_generator) == type(None):
                if self.get_image_from == 'directory':
                    train_datagen = self.create_image_data_generator(rescale = 1./255)
                else:
                    train_datagen = self.create_image_data_generator()
            else:
                train_datagen = image_data_generator
            if self.get_image_from == 'directory':
                self.compile_model(optimizer = optimizer, loss = keras.losses.categorical_crossentropy, metrics = metrics)
                train_generator = train_datagen.flow_from_directory(self.data_path, target_size = self.input_shape[:2], class_mode = 'categorical', batch_size = batch_size)
                num_dataset = 0
                for root, dirs, files in os.walk(self.data_path):
                    for basename in files:
                        file_extension = basename.split('.')[-1]
                        if file_extension in ('jpg', 'jpeg', 'png', 'bmp', 'ppm', 'tif', 'tiff'):
                            num_dataset += 1
                steps_per_epoch = ceil(num_dataset / batch_size)
                self.model.fit_generator(train_generator, steps_per_epoch=steps_per_epoch, epochs=epochs, verbose=verbose, callbacks=callbacks, shuffle=shuffle)
            elif self.get_image_from == 'argument':
                self.compile_model(optimizer = optimizer, loss = keras.losses.categorical_crossentropy, metrics = metrics)
                y_train = self.prepare_y(target_array, reverse_dict(self.model.class_indices), self.num_classes)
                train_generator = train_datagen.flow(x_train, y_train, batch_size = batch_size)
                num_dataset = x_train.shape[0]
                steps_per_epoch = ceil(num_dataset / batch_size)
                self.model.fit_generator(train_generator, steps_per_epoch=steps_per_epoch, epochs=epochs, verbose=verbose, callbacks=callbacks, shuffle=shuffle)


    def load(self, model_path = None, class_list_path = None):
        try:
            if type(model_path) == type(None):
                raise ValueError("Model path not exist")

            self.model = load_model(model_path)
            self.input_shape = self.model.input_shape[1:]
        except Exception as e:
            print("Model loading failed")
            raise e


    def save(self, model_path):
        try:
            if type(self.model) == type(None):
                raise TypeError('You should create a model before saving it')
            class_indice_list = list(self.class_indices.keys())
            save_model(self.model, model_path, class_indices = class_indice_list)
        except Exception as e:
            raise e


    def predict(self, data_array = None, data_path = None, predict_classes = True, batch_size = 32, verbose = 0, steps = None):
        try:
            if type(data_path) == type(None):
                raise TypeError('You sholud give a proper data path')
            test_img = cv2.imread(data_path)
            test_data = numpy.expand_dims(test_img, axis=0)
            data_array = self.reshape_data(test_data)

            probs = self.model.predict(data_array, batch_size = batch_size, verbose = verbose, steps = steps)
            if predict_classes == False:
                return probs
            predicted_classes = probs.argmax(axis=-1)
            output_dictionary = reverse_dict(self.model.class_indices)
            try:
                for i in range(predicted_classes.shape[0]):
                    if i == 0:
                        return_list = output_dictionary[predicted_classes[i]] 
                    else:
                        return_list.append(output_dictionary[predicted_classes[i]] )
                return numpy.asarray(return_list)
            except:
                return predicted_classes

        except Exception as e:
            raise e

    # TODO : have to implement evaluate function
    # def evaluate(self):



    def create_model(self):
        if type(self.model_type) == type(None):
            print("Default model will be resnet 50")
            self.model_type = 'resnet50'
        elif self.model_type == 'densenet121':
            if hasattr(self, 'input_shape') == False:
                self.input_shape = (224, 224, 3)
            self.model = densenet.DenseNet121( weights=None, input_shape=self.input_shape, classes=self.num_classes )
        elif self.model_type == 'inception_v3':
            if hasattr(self, 'input_shape') == False:
                self.input_shape = (299, 299, 3)
            self.model = inception_v3.InceptionV3( weights=None, input_shape=self.input_shape, classes=self.num_classes )
        elif self.model_type == 'inception_resnet_v2':
            if hasattr(self, 'input_shape') == False:
                self.input_shape = (299, 299, 3)
            self.model = inception_v3.InceptionV3( weights=None, input_shape=self.input_shape, classes=self.num_classes )
        elif self.model_type == 'mobilenet_v2':
            if hasattr(self, 'input_shape') == False:
                self.input_shape = (224, 224, 3)
            self.model = mobilenetv2.MobileNetV2( weights=None, input_shape=self.input_shape, classes=self.num_classes )
        elif self.model_type == 'nasnet_large':
            if hasattr(self, 'input_shape') == False:
                self.input_shape = (331, 331, 3)
            self.model = nasnet.NASNetLarge( weights=None, input_shape=self.input_shape, classes=self.num_classes )
        elif self.model_type == 'nasnet_mobile':
            if hasattr(self, 'input_shape') == False:
                self.input_shape = (224, 224, 3)
            self.model = nasnet.NASNetMobile( weights=None, input_shape=self.input_shape, classes=self.num_classes )
        elif self.model_type == 'xception':
            if hasattr(self, 'input_shape') == False:
                self.input_shape = (299, 299, 3)
            self.model = xception.Xception( weights=None, input_shape=self.input_shape, classes=self.num_classes )
        elif self.model_type == 'resnet50' :
            if hasattr(self, 'input_shape') == False:
                self.input_shape = (224, 224, 3)                   
            self.model = resnet50.ResNet50( weights=None, input_shape=self.input_shape, classes=self.num_classes)

        # Use multi gpu when available gpu is more than 1
        if self.gpu_num > 1:
            self.model = multi_gpu_model(self.model, gpus=self.gpu_num)

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


    def compile_model(self, optimizer, loss=None, metrics=['accuracy']):
        self.model.compile(optimizer, loss=loss, metrics=metrics)


    def init_output_dictionary_and_model(self):
        """Initializes self.model.
        
        Arguments:
            class_indices {dict} -- A reversed dictionary of output_dictionary.
            num_classes {int} -- A number of classes to classify.
        """
        self.create_model()
        return


    def prepare_y(self, target_array, class_indices, num_classes):
        """Prepares y for a keras model.(ex. y_train)
        
        Arguments:
            target_array {ndarray} -- ndarray. Appropriate outputs of input data.
            class_indices {dict} --
                A dictionary of classes to targets.
                (A reversed dictionary of self.model.output_dictionary)
            num_classes {int} -- A number of the entire classes.
        
        Returns:
            [ndarray] -- A binary matrix representation of the input.
        """
        y_list = list()
        for i in range(target_array.shape[0]):
            label_class = class_indices[target_array[i]]
            y_list.append(label_class)        
        y = keras.utils.to_categorical(numpy.asarray(y_list), num_classes)
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
        if data_array.shape[1:] != self.input_shape:
            reshaped_list = list()
            for i in range(data_array.shape[0]):
                resized_img = cv2.resize(data_array[i], (self.input_shape[0], self.input_shape[1]), interpolation = cv_interpolation)
                reshaped_list.append(resized_img)
            data_array = numpy.asarray(reshaped_list)
            reshaped_list = [] # empty list after use
        data_array = data_array.astype('float32')
        data_array /= 255
        return data_array
