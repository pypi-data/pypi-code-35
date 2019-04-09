import os
import cv2
import numpy as np
import tensorflow as tf
import math

from ....image_lib import split_one_image


RESHAPE = (512,512)

def is_an_image_file(filename):
    IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg']
    for ext in IMAGE_EXTENSIONS:
        if ext in filename:
            return True
    return False


def list_image_files(directory):
    files = sorted(os.listdir(directory))
    return [os.path.join(directory, f) for f in files if is_an_image_file(f)]


def load_image(path):
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    return img


def preprocess_image(img):
    resized_img = cv2.resize(img, RESHAPE)
    processed_img = (resized_img - 127.5) / 127.5
    return processed_img


def deprocess_image(img):
    img = img * 127.5 + 127.5
    return img.astype('uint8')


def load_images_data(path, n_images):
    if n_images < 0:
        n_images = float("inf")

    if os.path.isfile(path):
        all_image_paths = [path]
    elif os.path.isdir(path):
        all_image_paths = list_image_files(path)
    else:
        raise ValueError("path should be file or directory")

    images_all = []
    images_all_paths = []
    for path_image in all_image_paths:
        img = load_image(path_image)
        images_all.append(preprocess_image(img))
        images_all_paths.append(path_image)
        if len(images_all) > n_images - 1: break

    return {
        'images': np.array(images_all),
        'images_paths':images_all_paths
    }

def load_predict_images_data(path):
    if os.path.isfile(path):
        all_image_paths = [path]
    elif os.path.isdir(path):
        all_image_paths = list_image_files(path)
    else:
        raise ValueError("path should be file or directory")

    images_all = []
    images_all_paths = []
    images_all_area_index = []
    for path_image in all_image_paths:
        img = load_image(path_image)
        split_images, area_index = split_one_image(img, RESHAPE[0], RESHAPE[1])
        for i in range(len(split_images)):
            images_all.append(preprocess_image(split_images[i]))
            images_all_paths.append(path_image)
            images_all_area_index.append(area_index[i])

    return {
        'images': np.array(images_all),
        'images_paths':images_all_paths,
        'images_area_index': images_all_area_index
    }
