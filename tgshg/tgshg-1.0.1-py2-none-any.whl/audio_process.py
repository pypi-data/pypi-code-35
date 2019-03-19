#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
# Filename : audio_process.py
# author by :tgshg
# python2.7
# platform:visual studio code, windows 10 x64 in maya
# topic: maya plugins
# detial: process audio
# "Development Status :: 1 - Planning"
# "Development Status :: 2 - Pre-Alpha"
# "Development Status :: 4 - Beta  Copy classifier"
"""

import os
import subprocess
import wave
import contextlib
import warnings

import numpy as np
from audiolazy.lazy_lpc import lpc


class Error(Exception):
    pass


class MyCustomWarning(UserWarning):
    pass


def ffmpeg_extract_audio_from_video(out_path_audio,
                                    input_path_video,
                                    nchannels=1,
                                    framerate=16000):
    #Extract audio from the video
    cmd = 'ffmpeg -i %s -f wav -ac %s -ar %s -y -vn %s' % (
        input_path_video, nchannels, framerate, out_path_audio)
    subprocess.call(cmd)


def wave_read_data(file_path, read_seconds=None):
    with contextlib.closing(wave.open(file_path, 'r')) as f:
        params = f.getparams()
        nchannels, sampwidth, framerate, nframes = params[:4]

        if read_seconds:
            if (read_seconds * framerate) > nframes:
                raise Error, ("The number of seconds exceeds the maximum.")
            str_data = f.readframes(read_seconds * framerate)
        else:
            str_data = f.readframes(nframes)

        if sampwidth == 2:
            wave_data = np.fromstring(str_data, dtype=np.short)
        else:
            raise Error, ("The sampwidth of the wav file is not 2.")

        if nchannels == 2:
            warnings.warn(
                'The wav file is a single channel and the returned data is dual channel.',
                MyCustomWarning)
            wave_data.shape = -1, 2
            wave_data = wave_data.T

        return framerate, wave_data


def split_audio_chunks_of_520ms(input_path_wav,
                                frames_per_second=30,
                                chunks_length=0.260,
                                read_seconds=None):
    rate, signal = wave_read_data(input_path_wav, read_seconds=read_seconds)
    signal = signal / (2.**15)  # sampwidth=2
    number_of_frames = frames_per_second * (len(signal) / rate)
    frames_step_second = 1.0 / frames_per_second
    signal_skip_frames = int(1000 * chunks_length / frames_per_second)  # 8

    return [
        signal[int((i * frames_step_second - chunks_length) *
                   rate):int((i * frames_step_second + chunks_length) * rate)]
        for i in xrange(signal_skip_frames, number_of_frames -
                        signal_skip_frames + 1)
    ], number_of_frames, signal_skip_frames, rate


# The input audio window is divided into 64 audio frames with 2x overlap,
# so that each frame corresponds to 16ms (256 samples)
# and consecutive frames are located 8ms (128 samples) apart.
def divided_520ms_audio_frames_64x32_overlap(signal,
                                             fs=16000,
                                             overlap_frames_apart=0.008,
                                             lpc_order=32):
    overlap = int(fs * overlap_frames_apart)  # 16000*0.008 128 samples
    frame_size = int(fs * overlap_frames_apart * 2)  # 256 samples
    total_frames = int(abs(len(signal) - frame_size) / overlap) + 1
    # total_frames = 64
    frames = np.ndarray((total_frames, frame_size))
    for k in xrange(0, total_frames):
        for i in xrange(0, frame_size):
            if ((k * overlap + i) < len(signal)):
                frames[k][i] = signal[k * overlap + i]
            else:
                frames[k][i] = 0
    # remove the DC component
    frames = [(frames[k] - np.mean(frames[k]))
              for k in xrange(0, total_frames)]

    # apply the standard Hann window to reduce temporal aliasing effects
    frames *= np.hanning(frame_size)

    # calculate K = 32 autocorrelation coefficients to yield a total of 64×32 scalars for the input audio window.
    # if list is [0,0,0,...,0,0] or [0,0,0,...,0,1] ,lpc will return:[]
    frames_lpc_coefficient = []
    for i in xrange(0, total_frames):
        lpc_coefficient = lpc(frames[i], order=lpc_order).numerator[1:]
        if not len(lpc_coefficient) == lpc_order:
            lpc_coefficient = np.zeros((lpc_order))
        frames_lpc_coefficient.append(lpc_coefficient)

    return frames, frames_lpc_coefficient
