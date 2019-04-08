

from .support import name_and_ext, temporary_write, subprocess_call

def get_video_codec(input_path):
    cmd = f"ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 {input_path}"
    data = subprocess_call([x.strip() for x in cmd.split(' ') if x.strip()])
    data = [x for x in data.split('\n') if x.strip()][0].strip()
    try:
        return data
    except:
        return None
