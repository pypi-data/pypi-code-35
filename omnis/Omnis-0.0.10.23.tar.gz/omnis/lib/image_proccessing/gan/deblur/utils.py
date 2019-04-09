import os
from PIL import Image
import numpy as np
import tensorflow as tf
import math


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

def merge_image(img_list, images_area_index):
    # find biggest area
    largest_x = images_area_index[len(img_list) - 1][2]
    largest_y = images_area_index[len(img_list) - 1][3]
    BG = Image.new("RGB", (largest_x, largest_y))

    for i in range(len(img_list)):
        image_original_size = (images_area_index[i][2] - images_area_index[i][0], images_area_index[i][3] - images_area_index[i][1])
        image_after_resize = img_list[i].resize(image_original_size)
        BG.paste(image_after_resize, images_area_index[i])    

    return BG


def split_one_image(img, split_width, split_height):
    width, height = img.size
    x_count = math.ceil(width/split_width)
    y_count = math.ceil(height/split_height)

    split_image_list = []
    area_index = []
    for i in range(0, x_count):
        for j in range(0, y_count):
            x_start = i*split_width
            x_end = min((i+1)*split_width, width)
            y_start = j*split_height
            y_end = min((j+1)*split_height, height)
            area = (x_start, y_start, x_end, y_end)
            cropped_img = img.crop(area)
            split_image_list.append(cropped_img)
            area_index.append(area)
    
    return split_image_list, area_index



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
