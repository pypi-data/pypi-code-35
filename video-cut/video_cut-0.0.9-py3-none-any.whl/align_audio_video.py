from .support import name_and_ext, temporary_write, subprocess_call

def get_video_duration(input_path):
    cmd = f"ffprobe -v error -select_streams v:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1 {input_path}"
    data = subprocess_call([x.strip() for x in cmd.split(' ') if x.strip()])
    data = [x for x in data.split('\n') if x.strip()][0].strip()
    try:
        return float(data)
    except:
        return None

def get_audio_duration(input_path):
    cmd = f"ffprobe -v error -select_streams a:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1 {input_path}"
    data = subprocess_call([x.strip() for x in cmd.split(' ') if x.strip()])
    data = [x for x in data.split('\n') if x.strip()][0].strip()
    try:
        return float(data)
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

def extract_audio_subclip(filename, targetname, start, end, ):
    acodec = get_audio_codec(filename)
    cmd = [
      "ffmpeg","-y",
      "-i", filename,
      "-ss", "%0.3f" % (start),
      "-map","0:a",
      "-c:a", acodec,
      targetname
    ]
    subprocess_call(cmd)
    return targetname

def merge_audio_video(audio_path, video_path, out_path):
    cmd = [
      "ffmpeg","-y",
      "-i", audio_path,
      "-i", video_path,
      # "-strict",
      # "-2",
      # "-vcodec", "copy", "-acodec", "copy",
      "-map", "0:a",
      "-map", "1:v",
      "-c", "copy",
      # "-crf", "18",
      out_path
    ]
    subprocess_call(cmd)
    return out_path

def align_audio_video(in_path, out_path):
    v_duration = get_video_duration(in_path)
    a_duration = get_audio_duration(in_path)
    if not v_duration or not a_duration:
        return
    # if a_duration >= v_duration:
    name, ext = name_and_ext(in_path)
    with temporary_write('', path=f'{name}_temp_audio{ext}') as audio_path:
        start = a_duration - v_duration
        audio_path = extract_audio_subclip(in_path, audio_path, start, a_duration)
        out_path = merge_audio_video(audio_path, in_path, out_path)
        return out_path




if __name__ == '__main__':
    dur = get_audio_duration('/Users/morse/Documents/GitHub/twitch-to-youtube/data/videos/panetty_2019-04-07/./video_subclips/video_5.m2ts')
    print(dur)
