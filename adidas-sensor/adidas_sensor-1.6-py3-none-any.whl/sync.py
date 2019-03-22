import numpy as np
import pandas as pd
import sys


def read_csv(file):

    # load csv file
    tmp = pd.read_csv(file, delimiter=',', header=None)

    # convert to matrix
    data = tmp.values

    # get accelerometer
    acc = data[:, 1:4]

    # get gyroscope
    gyr = data[:, 5:8]

    return acc,gyr

def sync_video(
       csv_file: str,
       best_candidate_begin: float,
       best_candidate_end: float,
       video_synch_init: float,
       video_synch_end: float,
       sampling_rate:float = 500
    ):


    duration = video_synch_end - video_synch_init

    f_s_est = (best_candidate_end - best_candidate_begin) / duration

    if (abs(f_s_est - sampling_rate) <= 3.5):
        print('Estimated sampling rate is ok: {} Hz'.format(f_s_est))
    else:
        raise ValueError('Sampling rate is not correct')

    num_sam = best_candidate_end - best_candidate_begin + 1
    # set desired time axis
    time_video = np.arange(0, num_sam) * 1 / f_s_est
    time_video = time_video + video_synch_init

    acc,gyro = read_csv(csv_file)
    time_counter = 0
    counter = 0

    my_df = pd.DataFrame(columns=['acc_x','acc_y','acc_z','gyro_x','gyro_y','gyro_z','time'])
    
    for acc_data, gry_data in zip(acc, gyro):

        row_data = []
        row_data.append(acc_data[0])
        row_data.append(acc_data[1])
        row_data.append(acc_data[2])
        row_data.append(gry_data[0])
        row_data.append(gry_data[1])
        row_data.append(gry_data[2])

        if (counter >= best_candidate_begin and counter <= best_candidate_end):
            # update of time
            row_data.append(time_video[time_counter])
            time_counter = time_counter + 1
        else:
            row_data.append(0)

        my_df.loc[counter] = row_data
        counter = counter + 1
        

        
    return my_df


def main(args = sys.argv):
    arg_needed = 6
    pd = None
    if len(args) == arg_needed + 1:
       pd = sync_video(args[1], float(args[2]) ,float(args[3]) ,float(args[4]) ,float(args[5]) ,float(args[6])) 
    elif len(args) == arg_needed:
       pd = sync_video(args[1], float(args[2]) ,float(args[3]) ,float(args[4]) ,float(args[5])) 
    else:
        raise ValueError('Missing arguments')
    if pd is not None:
        pd.to_csv('synced_data.csv', sep=',', encoding='utf-8',index_label='sample')

if __name__ == '__main__':
    main()









