import math
import numpy as np


def generate_sound(filename,
                   fs=96000,  # number of samples per second (standard)
                   duration=1,  # seconds
                   frequency_left=1000,  # of cycles per second (Hz) (frequency of the sine wave for the left channel)
                   frequency_right=1000):  # of cycles per second (Hz) (frequency of the sine wave for the right channel)

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
