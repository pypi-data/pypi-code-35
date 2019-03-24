#!/usr/bin/env python
import os
import applescript
import public
import vlc.fullscreen
import vlc.time
import vlc.volume


@public.add
def tell(code):
    """execute applescript `tell application "VLC" ...`"""
    return applescript.tell.app("VLC", code).exc().out


@public.add
def duration():
    """return current video duration (seconds)"""
    if pid():
        return int(tell('duration of current item'))


@public.add
def path():
    """get current video path"""
    return tell('path of current item')


@public.add
def play(path=None, start=None):
    """open/continue play video"""
    if path:
        tell('open "%s"' % path)
        if start is not None:
            start = int(start) if int(start) > 0 else 1
            vlc.time.change(start)
    else:
        if not playing():
            tell('play')


@public.add
def pause():
    """pause current video"""
    if playing():
        tell('pause')


@public.add
def playing():
    """return True if video is playing"""
    return "true" in tell('playing') and int(tell('get current time')) > 0


"""
process functions
"""


@public.add
def activate():
    """open VLC and make it frontmost"""
    vlc.tell('activate')


@public.add
def frontmost():
    """return True if `VLC.app` is frontmost app, else False"""
    out = os.popen("lsappinfo info -only name `lsappinfo front`").read()
    return "VLC" in out.split('"')


@public.add
def pid():
    """VLC.app pid"""
    _pid = os.popen("pgrep VLC").read().strip()
    if _pid:
        return _pid


@public.add
def quit():
    """safe quit VLC"""
    if pid():
        vlc.tell("quit")


@public.add
def kill():
    """kill VLC.app process"""
    _pid = pid()
    if _pid:
        os.popen("kill -9 %s 2>&1" % _pid)
