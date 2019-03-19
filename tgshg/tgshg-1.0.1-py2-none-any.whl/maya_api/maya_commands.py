# -*- coding: UTF-8 -*-
"""
# Filename : maya_commands.py
# author by :tgshg
# python : 2.7
# platform : visual studio code, windows 10 x64 in maya
# topic : maya commands
# detial : maya all commands
# "Development Status :: 2 - Pre-Alpha"
# "Development Status :: 4 - Beta  Copy classifier"
"""
import maya.cmds as cmds
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as omanim
import maya.mel
import maya.utils as utils

import warnings

class Error(Exception):
    pass


class MyCustomWarning(UserWarning):
    pass


class PlayBackSliderPython:
    # To hear sound while scrubbing in the time slider, set the press and
    # release commands to begin and end sound scrubbing.

    def __init__(self):
        self.aPlayBackSliderPython = maya.mel.eval('$tmpVar=$gPlayBackSlider')

    def start_play(self):
        cmds.timeControl(self.aPlayBackSliderPython, edit=True, beginScrub=True)

    def stop_play(self):
        cmds.timeControl(self.aPlayBackSliderPython, edit=True, endScrub=True)


def get_frame_rate():
    current_unit = cmds.currentUnit(query=True, time=True)
    if current_unit.isalpha():
        return {
            'game': 15,
            'film': 24,
            'pal': 25,
            'ntsc': 30,
            "show": 48,
            'palf': 50,
            'ntscf': 60
        }.get(current_unit)
    else:
        raise Error, ('Only support for non-second based time units')


def set_frame_rate(fps=30):
    if fps in {
            'game': 15,
            'film': 24,
            'pal': 25,
            'ntsc': 30,
            "sh ow": 48,
            'palf': 50,
            'ntscf': 60
    }.values():
        cmds.currentUnit(time=(str(fps) + 'fps'))
    else:
        raise Error, ('Only support setting non-second based time units')


def get_mtime_unit():
    return omanim.MAnimControl.currentTime().unit


def get_mtime(mtime_value, mtime_unit=8):  # 30 frames per second (unit = 8)
    return om.MTime(mtime_value, mtime_unit)


def set_current_time(mtime_value=0, mtime_unit=8):
    omanim.MAnimControl.setCurrentTime(om.MTime(mtime_value, unit=mtime_unit))


def get_names_of_objects(all_object_specified_type='mesh'):
    # The ls command returns the names (and optionally the type names) of objects in the scene.
    return cmds.ls(type=all_object_specified_type)


def get_name_of_object(object_specified_type='mesh'):
    names = cmds.ls(type=object_specified_type)
    if len(names) == 0:
        warnings.warn("Can't find mesh", MyCustomWarning)
        return None
    elif len(names) > 1:
        warnings.warn("Multiple mesh objects, the default is the first one",
                      MyCustomWarning)
    return names[0]


def get_mesh(mesh_name=None):
    if mesh_name==None:
        mesh_name=get_name_of_object('mesh')
    cmds.select(mesh_name)
    mesh_list = om.MSelectionList()
    mesh_list.add(mesh_name)
    return om.MFnMesh(mesh_list.getDagPath(0))


def get_coordinate_space_constants(space='world_space'):
    """
    Coordinate Space Types
    int kInvalid = 0
    int kLast = 5
    int kObject = 2
    int kPostTransform = 3
    int kPreTransform = 2
    int kTransform = 1
    int kWorld = 4
    """
    return {
        'local_space': om.MSpace.kObject,
        'world_space': om.MSpace.kWorld
    }.get(space, om.MSpace.kWorld)


def get_animationEndTime():
    return int(cmds.playbackOptions(q=True, animationEndTime=True))


def get_animationStartTime():
    return int(cmds.playbackOptions(q=True, animationStartTime=True))


def get_maxtime():
    return int(cmds.playbackOptions(q=True, maxTime=True))


def get_mintime():
    return int(cmds.playbackOptions(q=True, minTime=True))


def set_animationEndTime(end_time=100):
    cmds.playbackOptions(animationEndTime=end_time)


def set_animationStartTime(start_time=0):
    cmds.playbackOptions(animationStartTime=start_time)


def set_maxtime(max_time=100):
    cmds.playbackOptions(maxTime=max_time)


def set_mintime(min_time=0):
    cmds.playbackOptions(minTime=min_time)


def set_mintime_maxtime(min_time=0, max_time=100):
    cmds.playbackOptions(minTime=min_time, maxTime=max_time)


def get_number_of_vertices():
    return int(cmds.polyEvaluate(vertex=True))
