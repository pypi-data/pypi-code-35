import math
import numpy as np


def generate_sound(filename=None, fs=96000, duration=1, frequency_left=1000, frequency_right=1000):
    """
    Helper method to dynamically generated a sound that can be used in with the Sound Card module.
    
    :param filename: (Optional)
    :param fs: (Optional) number of samples per second (standard)
    :param duration: (Optional) sound duration in seconds
    :param frequency_left: (Optional) number of cycles per second (Hz) (frequency of the sine wave for the left channel)
    :param frequency_right: (Optional) number of cycles per second (Hz) (frequency of the sine wave for the right channel)
    :return: Returns the **flatten** generated sound as a numpy array (as np.int8)
    """

    amplitude24bits = math.pow(2, 31) - 1

    samples = np.arange(0, duration, 1 / fs)
    wave_left = amplitude24bits * np.sin(2 * math.pi * frequency_left * samples)
    wave_right = amplitude24bits * np.sin(2 * math.pi * frequency_right * samples)

    stereo = np.stack((wave_left, wave_right), axis=1)

    wave_int = stereo.astype(np.int32)

    if filename:
        with open(filename, 'wb') as f:
            wave_int.tofile(f)

    return wave_int.flatten()
