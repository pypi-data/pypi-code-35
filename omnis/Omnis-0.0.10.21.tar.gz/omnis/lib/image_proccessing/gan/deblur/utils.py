import os
from PIL import Image
import numpy as np
import tensorflow as tf


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
    img = Image.open(path)
    return img


def preprocess_image(cv_img):
    cv_img = cv_img.resize(RESHAPE)
    img = np.array(cv_img)
    img = (img - 127.5) / 127.5
    return img


def deprocess_image(img):
    img = img * 127.5 + 127.5
    return img.astype('uint8')


def save_image(np_arr, path):
    img = np_arr * 127.5 + 127.5
    im = Image.fromarray(img)
    im.save(path)


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

def write_log(callback, names, logs, batch_no):
    """
    Util to write callback for Keras training
    """
    for name, value in zip(names, logs):
        summary = tf.Summary()
        summary_value = summary.value.add()
        summary_value.simple_value = value
        summary_value.tag = name
        callback.writer.add_summary(summary, batch_no)
        callback.writer.flush()
