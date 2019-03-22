import numpy as np


def sync_video(best_candidate_begin: float,
               best_candidate_end: float,
               video_synch_init: float,
               video_synch_end: float):


    duration = video_synch_end - video_synch_init

    f_s_est = (best_candidate_end - best_candidate_begin) / duration

    if (abs(f_s_est - 200) <= 3.5):
        print('Estimated sampling rate is ok: {} Hz'.format(f_s_est))

    num_sam = best_candidate_end - best_candidate_begin + 1
    # set desired time axis
    time_video = np.arange(0, num_sam) * 1 / f_s_est
    time_video = time_video + video_synch_init

    return time_video
