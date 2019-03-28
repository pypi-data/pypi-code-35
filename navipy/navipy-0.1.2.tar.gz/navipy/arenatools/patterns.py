"""
Tools to generate patterns
"""
import numpy as np


def generate_1overf_noise(img_size, beta, noise=None):
    """
    Generates the discrete fourier transformation of noise and weights it with weights<0.
    Where the smallest weights are in the middle columns of the returned noise array and the biggest in the outer columns.
    First generates the noise and applies the following formula:

    .. math::

            DFT(\\frac{1}{f^{\\beta}} * DFT(noise))

    The noise must be a 2d array.

    :params img_size: size of the output noise dimensions \
(array dimension e.g. (4,4))
    :params beta: used to calculate the weights of the noise, \
the bigger beta the smaller the weights, can have an arbitrary value \
(weights are always between 0 and 1)
    :params noise: array with same size as img_size, that is used as \
the noise (default: random generated noise)
    """
    # Calculate image size -> next biggest power of two,
    # in which the image fits (s>=max(img_size))
    s = 2**(np.ceil(np.log2(np.max(img_size)))).astype(int)
    if noise is None:
        # generate white noise
        noise = np.random.randn(s, s)

    # calculate filter
    fx = np.arange(s/2)+1
    # index from 0-s/2,s/2-0 -> middle highest index
    fx = np.hstack([fx, fx[-1::-1]])
    fx = fx[:, np.newaxis]
    # copy first row s times -> fx=[[0..0],[1..],..,[s/2,..s/2],..[0..0]
    # fx is a symmetric matrix
    fx = fx.repeat(s, axis=1)
    fy = fx.transpose()

    f = np.sqrt(fx**2 + fy**2)  # Euclidian norm
    f = f**(-beta)
    # apply filter in frequency domain
    # calculate disrete furier transformations
    fnoise = np.fft.ifft2(np.fft.fft2(noise)*f)

    # trim to image size
    fnoise = fnoise[:img_size[0], :img_size[1]]
    fnoise = np.real(fnoise)
    return fnoise


def gray2red(img):
    """ convert a gray image to a red image (black -> red)

    Many bees and flies are not sensitive to red light, and
    can be better observed on red background than on a black one
    due to their dark colour.

    :params img: Gray image to be converted into red-white one
    """
    img = img[..., np.newaxis]
    img = img.repeat(3, axis=2)
    maxval = np.max(img)
    img[:, :, 1] = maxval-img[:, :, 0]
    img[:, :, 2] = maxval-img[:, :, 0]
    img[:, :, 0] = maxval
    return img


def norm_img(img):
    """ Normalise an 8bit image between 0 and 255

    :params img: Image to be normalised
    """
    img = img.astype(np.float)
    img -= img.min()
    img /= img.max()
    img *= 255
    return img.astype(np.uint8)


def rectangular_pattern(width, length, beta=1.4, pixel_per_mm=1):
    """generate a rectangular pattern

    :param width: width of the pattern in mm
    :param length: length of the pattern in mm
    :param beta: beta coef for generating a 1/(f^beta) pattern
    :param pixel_per_mm: number of pixel per mm
    :returns: a rectangular random image
    :rtype: np.ndarray
    """
    corridor = np.array([width, length])
    corridor_px = corridor*pixel_per_mm  # in px
    return generate_1overf_noise(corridor_px, beta)
