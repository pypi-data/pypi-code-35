from __future__ import print_function

"""
File for general functions
"""
import sys; import os
import subprocess
import numpy as np
from util import (is_iterable)


def run(cmd):
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output


def find_conditions(m, shouldbe_m):
    """
    creates a list where the condition matrix
    corresponds to True/False

    m: np.array, domain -> [True, False]
    shouldbe_m: element-wise comparison truth
    """
    indices = []
    for i, row in enumerate(m):
        for j, elem in enumerate(row):
            if is_iterable(obj=elem):

                if not np.array_equal(elem,
                                      shouldbe_m[i, j]):
                    indices.append(tuple([i, j]))

            elif str(elem) == str(shouldbe_m[i, j]):
                indices.append(tuple([i, j]))

    return indices


def copy_file_to_docker_host(docker_fp, host_dir):
    """
    function to copy a file from docker_fp to host_dir/docker_fn

    Works only on *nix (/)
    """
    docker_fn = docker_fp.split('/')[-1]
    host_fp = os.path.join(host_dir, docker_fn)
    cmd = 'cp {docker_fp} {host_fp}'
    cmd = cmd.format(docker_fp=docker_fp,
                     host_fp=host_fp)
    run(cmd, shell=True, check=True)

def print_image_frame_data(image_name, image):
    print('[{}]'.format(image_name))
    print('\t', 'data dimensions:', image.shape)
    print('\t', 'Top level type:', type(image))
    print('\t', 'Row level type:', type(image[0]))
    print('\t', 'Color Channel level type:', type(image[0][0]))
    print('\t', 'RGB Val level type:', type(image[0][0][0]))


def unpack_bytes_image(bytes_object, image_shape):
    out = array.array('B', bytes_object)
    out = np.array(out, dtype=np.uint8)
    return np.reshape(out, newshape=image_shape)


def create_bytes_image(frame_data):
    return frame_data.tobytes('C')


def create_json(frame_data):
    payload = {
        'frame': frame_data.tolist(),
    }
    return json.dumps(payload)

def unpack_json(json_string):
    try:
        image = json.loads(json_string)
    except Exception as e:
        print('BAD JSON STR', json_string)
        raise e
    image = np.array(image['frame'],
                     dtype=np.uint8)
    return image
