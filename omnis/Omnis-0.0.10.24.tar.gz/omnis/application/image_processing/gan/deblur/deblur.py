import numpy as np
import os

import keras
import cv2
from keras.optimizers import Adam

from .....lib.image_lib import merge_image
from .....lib.image_proccessing.gan.deblur.model import generator_model, discriminator_model, generator_containing_discriminator_multiple_outputs
from .....lib.image_proccessing.gan.deblur.utils import load_images_data, deprocess_image, load_predict_images_data
from .....lib.image_proccessing.gan.deblur.losses import wasserstein_loss, perceptual_loss

from ....application import Application

class Deblur_GAN(Application):
    def __init__(self, g_model_path = None, d_model_path = None):
        super().__init__()

        self.create_model()

        if type(g_model_path) != type(None):
            if type(d_model_path) != type(None):
                self.load(g_model_path = g_model_path, d_model_path = d_model_path)
            else:
                self.load_g_model(model_path = g_model_path)
    
    def prepare_train_data(self, data_path):
        self.blur_data_path = os.path.join(data_path, 'blur')
        self.sharp_data_path = os.path.join(data_path, 'sharp')


    def train(self, batch_size=1, epochs = 1, critic_updates = 5):
        data_blur = load_images_data(self.blur_data_path, batch_size)
        data_sharp = load_images_data(self.sharp_data_path, batch_size)

        blur_image_array = data_blur['images']
        sharp_image_array = data_sharp['images']

        d_on_g = generator_containing_discriminator_multiple_outputs(self.g_model, self.d_model)


        d_opt = Adam(lr=1E-4, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
        d_on_g_opt = Adam(lr=1E-4, beta_1=0.9, beta_2=0.999, epsilon=1e-08)

        self.d_model.trainable = True
        self.d_model.compile(optimizer=d_opt, loss=wasserstein_loss)
        self.d_model.trainable = False
        loss = [perceptual_loss, wasserstein_loss]
        loss_weights = [100, 1]
        d_on_g.compile(optimizer=d_on_g_opt, loss=loss, loss_weights=loss_weights)
        self.d_model.trainable = True

        output_true_batch, output_false_batch = np.ones((batch_size, 1)), -np.ones((batch_size, 1))

        log_path = './logs'

        for epoch in range(0, epochs):
            permutated_indexes = np.random.permutation(blur_image_array.shape[0])

            d_losses = []
            d_on_g_losses = []
            for index in range(int(blur_image_array.shape[0] / batch_size)):
                batch_indexes = permutated_indexes[index*batch_size:(index+1)*batch_size]
                image_blur_batch = blur_image_array[batch_indexes]
                image_full_batch = sharp_image_array[batch_indexes]

                generated_images = self.g_model.predict(x=image_blur_batch, batch_size=batch_size)

                for _ in range(critic_updates):
                    d_loss_real = self.d_model.train_on_batch(image_full_batch, output_true_batch)
                    d_loss_fake = self.d_model.train_on_batch(generated_images, output_false_batch)
                    d_loss = 0.5 * np.add(d_loss_fake, d_loss_real)
                    d_losses.append(d_loss)

                self.d_model.trainable = False

                d_on_g_loss = d_on_g.train_on_batch(image_blur_batch, [image_full_batch, output_true_batch])
                d_on_g_losses.append(d_on_g_loss)

                self.d_model.trainable = True
            print(np.mean(d_losses), np.mean(d_on_g_losses))



    def save(self, g_model_path, d_model_path):
        try:
            self.save_g_model(g_model_path)
            self.save_d_model(d_model_path)
        except Exception as e:
            raise e

    
    def load(self, g_model_path, d_model_path):
        try:
            self.load_g_model(g_model_path)
            self.load_d_model(d_model_path)
        except Exception as e:
            raise e
        

    def predict(self, data_path, batch_size = 1, saved_path = 'results'):
        image_data = load_predict_images_data(data_path)
        image_array = image_data['images']
        image_paths_list = image_data['images_paths']
        image_area_index = image_data['images_area_index']

        generated_images = self.g_model.predict(x=image_array, batch_size = batch_size)
        generated_images_array = np.array([deprocess_image(img) for img in generated_images])

        image_list = []
        for i in range(generated_images.shape[0]):
            img = generated_images_array[i, :, :, :]
            image_list.append(img)

        now_image_path = image_paths_list[0]
        merge_image_list = []
        merge_image_area_list = []
        for i in range(len(image_paths_list)):
            if image_paths_list[i] != now_image_path:
                merged_image = merge_image(merge_image_list, merge_image_area_list)
                self.save_merged_image(merged_image, saved_path, data_path, now_image_path)
                now_image_path = image_paths_list[i]
                merge_image_list = []
                merge_image_area_list = []
            merge_image_list.append(image_list[i])
            merge_image_area_list.append(image_area_index[i])

            if i == len(image_paths_list) - 1:
                merged_image = merge_image(merge_image_list, merge_image_area_list)
                self.save_merged_image(merged_image, saved_path, data_path, now_image_path)


    def save_merged_image(self, image, saved_path, data_path, now_image_path):
        filename = os.path.basename(data_path)
        if not os.path.exists(saved_path):
            os.makedirs(saved_path)
        if os.path.isdir(data_path):
            if not os.path.exists(os.path.join(saved_path, data_path)):
                os.makedirs(os.path.join(saved_path, data_path))
            cv2.imwrite(os.path.join(saved_path, now_image_path), image)
        else:
            cv2.imwrite(os.path.join(saved_path, filename),image)


    def create_model(self):
        self.g_model = self.create_g_model()
        self.d_model = self.create_d_model()


    def create_g_model(self):
        g_model = generator_model()
        return g_model


    def create_d_model(self):
        d_model = discriminator_model()
        return d_model


    def load_g_model(self, model_path):
        self.g_model.load_weights(model_path)


    def load_d_model(self, model_path):
        self.d_model.load_weights(model_path)


    def save_g_model(self, model_path):
        self.g_model.save_weights(model_path)


    def save_d_model(self, model_path):
        self.d_model.save_weights(model_path)


    