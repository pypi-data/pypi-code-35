import os
ffmpegpath = os.path.abspath(os.path.dirname(__file__))


def export_ffmpeg_path():
    os.environ["PATH"] += os.pathsep + ffmpegpath
    pass
