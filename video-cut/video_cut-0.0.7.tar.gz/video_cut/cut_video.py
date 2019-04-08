import os.path
from .support import subprocess_call
from .align_audio_video import align_audio_video
from .support import name_and_ext, temporary_write

def get_video_codec(input_path):
    cmd = f"ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 {input_path}"
    data = subprocess_call([x.strip() for x in cmd.split(' ') if x.strip()])
    data = [x for x in data.split('\n') if x.strip()][0].strip()
    try:
        return data
    except:
        return None

def get_audio_codec(input_path):
    cmd = f"ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 {input_path}"
    data = subprocess_call([x.strip() for x in cmd.split(' ') if x.strip()])
    data = [x for x in data.split('\n') if x.strip()][0].strip()
    try:
        return data
    except:
        return None


def cut_video(in_path, out_path, start, end, encode=False):
    name, ext = name_and_ext(out_path)
    if end - start > 4 and not encode:
        with temporary_write('', path=f'_{name}{ext}') as temp_path:
            cmd = [
              "ffmpeg","-y",
              "-i", in_path,
              "-ss", "%0.3f" % start,
              "-to", "%0.3f" % end,
              "-map","0",
              "-c", "copy",
              "-shortest",
              "-avoid_negative_ts", "1",
              temp_path
            ]
            subprocess_call(cmd)
            out_path = align_audio_video(temp_path, out_path)
            return out_path
    else:
        vcodec = get_video_codec(in_path)
        acodec = get_audio_codec(in_path)
        cmd = [
          "ffmpeg","-y",
          "-i", in_path,
          "-ss", "%0.3f" % start,
          "-to", "%0.3f" % end,
          "-map","0",
          "-c:v", vcodec,
          "-c:a", acodec,
          "-shortest",
          "-crf", "18",
          "-avoid_negative_ts", "1",
          out_path
        ]
        subprocess_call(cmd)
        return out_path
