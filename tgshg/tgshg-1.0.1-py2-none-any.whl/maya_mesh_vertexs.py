# -*- coding: UTF-8 -*-
"""
# Filename : maya_mesh_vertexs.py
# author by :tgshg
# python : 2.7
# platform : visual studio code, windows 10 x64 in maya
# topic : maya plugins
# detial : mesh vertexs save and write
# "Development Status :: 1 - Planning"
# "Development Status :: 2 - Pre-Alpha"
# "Development Status :: 3 - Alpha  Copy classifier"
# "Development Status :: 4 - Beta  Copy classifier"
"""

import threading
import time
import warnings
import contextlib

from . import maya_commands as adsk
import numpy as np


class Error(Exception):
    pass


class MyCustomWarning(UserWarning):
    pass


class MeshVertexs(object):  # class A(object): python2 必须显示地继承object
    def __new__(cls):
        mesh_name = adsk.get_name_of_object(object_specified_type='mesh')
        if not mesh_name:
            return None
        return super(MeshVertexs, cls).__new__(cls)

    def __init__(self):
        # mesh_name = adsk.get_name_of_object(object_specified_type='mesh')
        self.mesh = adsk.get_mesh()  #mesh_name
        self.total_vertexs = adsk.get_number_of_vertices()
        self.total_frame = adsk.get_maxtime() + 1
        self.maya_fps = adsk.get_frame_rate()

        super(MeshVertexs, self).__init__()

    def get_mesh_name(self):
        self.mesh_name = adsk.get_name_of_object()
        return self.mesh_name

    def get_maya_fps(self):
        return self.maya_fps

    def get_mesh_number_vertexs(self):
        return self.total_vertexs

    def get_total_frame(self):
        return self.total_frame

    def export_vertexs_npy(self,
                           file_path,
                           space='world_space',
                           time_min=0,
                           time_max=None):
        if (time_max == None) or (time_max >= self.total_frame):
            warnings.warn("Maximum time is not set or exceeds maximum setting",
                          MyCustomWarning)
            time_max = self.total_frame - 1
        if (time_min < adsk.get_mintime()):
            warnings.warn("The shortest time exceeds the minimum setting",
                          MyCustomWarning)
            time_min = adsk.get_mintime()

        space = adsk.get_coordinate_space_constants(space=space)
        time_unit = adsk.get_mtime_unit()

        # vertexs = [time,vertexs,[x y z]]
        vertexs = np.ndarray(
            shape=(time_max + 1, self.total_vertexs, 3), dtype=float)
        for frame in xrange(time_min, time_max):
            adsk.set_current_time(frame, time_unit)
            points = self.mesh.getPoints(space)
            for i in xrange(0, len(points)):
                vertexs[frame][i] = [points[i][0], points[i][1], points[i][2]]
        np.save(file_path, vertexs)

    class ImportVertexs:
        def __init__(self,
                     file_path=None,
                     time_start=0,
                     time_stop=None,
                     mesh_name=None,
                     space='world_space'):
            self.file_path = file_path
            self.time_start = time_start
            self.time_stop = time_stop
            self.space = adsk.get_coordinate_space_constants(space=space)
            self.mesh = adsk.get_mesh(mesh_name=mesh_name)

            self.thread_is_alive = False
            self.playback_slider_check()

        def playback_slider_check(self):
            self.vertexs = np.load(self.file_path)
            total_frame = len(self.vertexs)
            self.total_vertexs = len(self.vertexs[0])
            number_of_vertices = adsk.get_number_of_vertices()
            if not (self.total_vertexs == number_of_vertices):
                raise Error, (
                    "The number of vertices is different from the number in the scene"
                )

            if 0 < adsk.get_mintime():
                adsk.set_mintime(0)
            if self.time_start < adsk.get_mintime():
                warnings.warn(
                    "Play start time exceeds minimum setting (default play time starts from zero)",
                    MyCustomWarning)
                self.time_start = adsk.get_mintime()

            if self.time_stop == None:
                self.time_stop = total_frame - 1 + self.time_start
            if self.time_stop < self.time_start:
                raise Error, ("Play stop time is greater than start time")
            if self.time_stop > (total_frame - 1 + self.time_start):
                warnings.warn(
                    "Stop playing time exceeds the maximum supported by data",
                    MyCustomWarning)
                self.time_stop = total_frame - 1 + self.time_start
            if self.time_stop > adsk.get_maxtime():
                warnings.warn(
                    "Stop playback time exceeds playback range, set playback range to stop playback time",
                    MyCustomWarning)
                adsk.set_maxtime(self.time_stop)

        def import_vertexs(self):
            self.current_time = self.time_start
            fps = adsk.get_frame_rate()
            time_unit = adsk.get_mtime_unit()
            ofps = float(1.0 / fps)  # One frame per second
            self.play_wav_frame.start_play()

            def writing_vertexs():
                if (self.current_time > self.time_stop):
                    if self.thread.isAlive():
                        self.import_stop()
                elif self.thread.isAlive():
                    adsk.set_current_time(self.current_time, time_unit)
                    points = adsk.om.MPointArray()
                    for v in xrange(0, self.total_vertexs):
                        points.append(self.vertexs[self.current_time][v])
                    self.mesh.setPoints(points, self.space)

                    self.current_time += 1

            while self.thread_is_alive:
                time.sleep(ofps)
                adsk.utils.executeDeferred(writing_vertexs)

        def import_start(self):
            self.play_wav_frame = adsk.PlayBackSliderPython()
            self.thread_is_alive = True
            self.thread = thread = threading.Thread(
                None, target=self.import_vertexs)
            self.thread.start()

        def import_stop(self):
            self.thread_is_alive = False
            self.play_wav_frame.stop_play()
