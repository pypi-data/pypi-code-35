# Copyright 2018-2019 Ori Ben-Moshe - All rights reserved.
import cv2
import numpy as np


def validate_odd_size(size):
    """
    Action: validates that a kernel shape is of odd  ints and of size 2
    :param size: the shape (size) to be checked
    :return: doesnt raise an error if it's ok.
    """
    if type(size) not in (list, tuple):
        raise TypeError("Kernel size must be a tuple or list of 2 odd integers!")
    if len(size) != 2:
        raise ValueError("Kernel size must be a tuple or list of 2 odd integers!")
    if size[0] % 2 != 1 or size[1] % 2 != 1:
        raise ValueError("Kernel size must be 2 odd integers!")


def is_odd_size(size):
    """
    Action: validates that a kernel shape is of odd  ints and of size 2
    :param size: the shape (size) to be checked
    :return: doesnt raise an error if it's ok.
    """
    if type(size) not in (list, tuple):
        return False
    if len(size) != 2:
        return False
    if size[0] % 2 != 1 or size[1] % 2 != 1:
        return False
    return True


def validate_kernel(size):
    """
    Action: Validates the Size of a kernel
    :param size: the size (shape)
    :return:
    """
    if type(size) not in (list, tuple):
        raise TypeError("Kernel size must be a tuple or list!")
    if len(size) != 2:
        raise ValueError("Kernel size must be a tuple or list!")
    for i in size:
        if type(i) is not int:
            raise TypeError("Size must consist only of ints")


def cross_kernel(size):
    """
    Action: Returns a cross (ones in a cross) kernel for morphological functions
    Example of a (5,5) cross:
    | 0 0 1 0 0 |
    | 0 0 1 0 0 |
    | 1 1 1 1 1 |
    | 0 0 1 0 0 |
    | 0 0 1 0 0 |
    :param size:  a tuple of size 2 of 2 odd integers denoting the size of the kernel
    f.g. (5, 5)
    :return: the numpy.array of the cross shape
    """
    validate_odd_size(size)
    return cv2.getStructuringElement(cv2.MORPH_CROSS, ksize=size)


def rectangle_kernel(size):
    """
    Action: Returns a rectangle (all ones) kernel for morphological functions
    Example of a (5,5) rectangle:
    | 1 1 1 1 1 |
    | 1 1 1 1 1 |
    | 1 1 1 1 1 |
    | 1 1 1 1 1 |
    | 1 1 1 1 1 |
    :param size:  a tuple of size 2 of 2 odd integers denoting the size of the kernel
    f.g. (5, 5)
    :return: the numpy.array of the cross shape
    """
    return cv2.getStructuringElement(cv2.MORPH_RECT, ksize=size)


def ellipse_kernel(size):
    """
    Action: Returns an ellipse (ones in the shape of an ellipse) kernel for morphological functions
    Example of a (5,5) ellipse:
    | 0 0 1 0 0 |
    | 1 1 1 1 1 |
    | 1 1 1 1 1 |
    | 1 1 1 1 1 |
    | 0 0 1 0 0 |
    :param size: a tuple of size 2 of 2 odd integers denoting the size of the kernel
    f.g. (5, 5)
    :return: the kernel
    """
    validate_odd_size(size)
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize=size)


def horizontal_line_kernel(size):
    """
    Action: Returns an horizontal line (a horizontal line of ones) kernel for morphological functions
    Example of a (5,5) horizontal line:
    | 0 0 0 0 0 |
    | 0 0 0 0 0 |
    | 1 1 1 1 1 |
    | 0 0 0 0 0 |
    | 0 0 0 0 0 |
    :param size: a tuple of size 2 of 2 odd integers denoting the size of the kernel
    f.g. (5, 5)
    :return: the kernel
    """
    validate_odd_size(size)
    arr = np.zeros(size, dtype=np.uint8)
    arr[int((size[0] - 1) / 2), ] = 1
    return arr


def vertical_line_kernel(size):
    """
    Action: Returns a vertical line (a vertical line of ones) kernel for morphological functions
    Example of a (5,5) vertical line:
    | 0 0 1 0 0 |
    | 0 0 1 0 0 |
    | 0 0 1 0 0 |
    | 0 0 1 0 0 |
    | 0 0 1 0 0 |

    :param size: a tuple of size 2 of 2 odd integers denoting the size of the kernel
    f.g. (5, 5)
    :return: the kernel
    """
    validate_odd_size(size)
    arr = np.zeros(size, dtype=np.uint8)
    arr[:, int((size[1] - 1) / 2)] = 1
    return arr


def convert_to_hsv(img):
    """
    Action: converts an image to hsv - Mainly for beginner use
    :param img: image to be converted
    :return: the converted image
    """
    return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


def erosion(mask, kernel=rectangle_kernel((5, 5)),
            iterations=None, destination=None, anchor=None,
            border_type=None, border_values=None):
    """
    Action: a copy of cv2.erode with default kernel of 5 by 5
    (a logical operation on the binary mask,
    whether every pixel's value should stay as it is based on neighboring pixels,
    which neighbors are chosen by the kernel and its dimensions)
    Erode demands all chosen neighbors must be True (white)
    For more information:
    https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html

    :param mask: the binary image where the erosion morphological function should be applied
    :param kernel: the kernel that should be used
    :param iterations: Number of times the function should be applied
    :param destination: where the new image should be saved
    :param anchor: position of the anchor within the element
    :param border_values: border value in case of a constant border
    :param border_type: Pixel extrapolation technique for the border of the image
    see: https://docs.opencv.org/3.4.2/d2/de8/group__core__array.html#ga209f2f4869e304c82d07739337eae7c5
    :return: the eroded binary mask
    """
    return cv2.erode(mask,
                     kernel,
                     dst=destination,
                     anchor=anchor,
                     iterations=iterations,
                     borderValue=border_values,
                     borderType=border_type)


def dilation(mask, kernel=rectangle_kernel((5, 5)),
             iterations=None, destination=None, anchor=None,
             border_type=None, border_values=None):
    """
    Action: a copy of cv2.dilate with default kernel of 5 by 5
    (a logical operation on the binary mask,
    whether every pixel's value should stay as it is based on neighboring pixels,
    which neighbors are chosen by the kernel and its dimensions)
    Dilation demands at least one chosen neighbors must be True (white)
    For more information:
    https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html

    :param mask: the binary image where the erosion morphological function should be applied
    :param kernel: the kernel that should be used
    :param iterations: Number of times the function should be applied
    :param destination: where the new image should be saved
    :param anchor: position of the anchor within the element
    :param border_values: border value in case of a constant border
    :param border_type: Pixel extrapolation technique for the border of the image
    see: https://docs.opencv.org/3.4.2/d2/de8/group__core__array.html#ga209f2f4869e304c82d07739337eae7c5
    :return: the dilated binary mask
    """
    return cv2.dilate(mask,
                      kernel,
                      dst=destination,
                      anchor=anchor,
                      iterations=iterations,
                      borderValue=border_values,
                      borderType=border_type)


def sharpen_image(image, size=(3, 3)):
    """
    Action: Sharpens an image by preforming convolution it with a sharpening matrix
    :param image: the image (ndarray)
    :param size: the size of the sharpening matrix
    :return: the new sharpened image
    """

    validate_odd_size(size)
    kernel = np.ones(size)
    kernel *= -1
    kernel[int((size[0] - 1) / 2), int((size[1] - 1) / 2)] = kernel.size
    return cv2.filter2D(image, -1, kernel)


def adaptive_brightness(image, brightness=127, hsv=False):
    """
    Action: Changes the brightness of every pixel so that the average is the target average
    :param image: The image to be changed (Numpy array)
    :param brightness: the target average for the image
    :type brightness: int (int between 0 - 255)
    :param hsv: bool noting if the image is in hsv
    :return: a copy of the image changed
    """
    image = image if hsv else cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    brightness = brightness * 2.55
    img_h_mean = cv2.mean(image)[2]
    increase = brightness - img_h_mean
    vid = image[:, :, 2]
    if increase > 0:
        vid = np.where(vid + increase <= 255, vid + increase, 255)
    else:
        vid = np.where(vid + increase >= 0, vid + increase, 0)
    image[:, :, 2] = vid
    image = image if hsv else cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
    return image


def change_brightness(image, change,  hsv=False):
    """
    Action: Changes the brightness of every pixel of a BGR image by the given amount
    :param image: The image to be changed (Numpy array)
    :param change: the change (integer)
    :type change: int
    :param hsv: bool noting if the image is in hsv
    :return: a copy of the image changed
    """
    image = image if hsv else cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    change = change * 2.55
    vid = image[:, :, 2]
    if change > 0:
        vid = np.where(vid + change <= 255, vid + change, 255)
    else:
        vid = np.where(vid + change >= 0, vid + change, 0)
    image[:, :, 2] = vid
    image = image if hsv else cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
    return image


def rotate_by_angle(image, angle):
    """
    Action: rotates the given image by a given angle
    :param image: the image to be rotated
    :param angle: the angle of rotation
    :return: the rotated image
    """
    (h, w) = image.shape[:2]
    center_xy = (w / 2, h / 2)
    rotation_matrix = cv2.getRotationMatrix2D(center_xy, -angle, 1.0)
    cos = np.abs(rotation_matrix[0, 0])
    sin = np.abs(rotation_matrix[0, 1])
    new_image_dimensions = (int((h * sin) + (w * cos)), int((h * cos) + (w * sin)))
    rotation_matrix[0, 2] += (new_image_dimensions[0] / 2) - center_xy[0]
    rotation_matrix[1, 2] += (new_image_dimensions[1] / 2) - center_xy[1]
    return cv2.warpAffine(image, rotation_matrix, new_image_dimensions)


def rotate90_left(image):
    """
    Action: return a copy of the image rotated 90 degrees to the left (counter-clockwise)
    :param image: numpy array, image to be rotated
    :return: a copy of the image rotated.
    """
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, 90, 1.0)
    return cv2.warpAffine(image, rotation_matrix, (h, w))


def rotate90_right(image):
    """
    Action: return a copy of the image rotated 90 degrees to the right (clockwise)
    :param image: numpy array, image to be rotated
    :return:
    """
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, 270, 1.0)
    return cv2.warpAffine(image, rotation_matrix, (h, w))


def rotate180(image):
    """
    Action: return a copy of the image rotated 180
    :param image:  numpy array, image to be rotated
    :return: a copy of the image rotated.
    """
    (h, w) = image.shape[:2]
    center = (w / 2, h / 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, 180, 1.0)
    return cv2.warpAffine(image, rotation_matrix, (h, w))
