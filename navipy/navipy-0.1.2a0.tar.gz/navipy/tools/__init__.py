"""
Some tools
"""
import pandas as pd
import numpy as np


def extract_block(data, thresholds):
    """
        data is a pandas series with integer consecutive indexes

        return a dataframe, index by block containing block start and end
        a block is defined as:
            - data are greater than threshold_1
            - extend to the last value of data below threshold_2 \
before the block
            - extend to the first value of data below threshold_2 \
after the block

        threshold_1 should be higher than threshold_2
    """
    threshold_2 = min(thresholds)
    threshold_1 = max(thresholds)

    # create a dataframe containing:
    # in column th_1: 1 for data above th_1, nan other wise
    # in column th_2: 1 for data below th_2, nan other wise
    treshold_df = pd.DataFrame(index=data.index,
                               columns=['th_1', 'th_2'])
    treshold_df.th_1[data > threshold_1] = 1
    treshold_df.th_2[data <= threshold_2] = 1
    treshold_df['frame'] = treshold_df.index
    # Calculate unextended block
    subdf = treshold_df[['th_1', 'frame']].dropna(how='any')
    start_block = subdf.frame[(subdf.frame.diff() > 1)
                              | (subdf.frame.diff().isnull())]
    end_block = subdf.frame[(subdf.frame[::-1].diff() < -1)
                            | (subdf.frame[::-1].diff().isnull())]

    block_df = pd.DataFrame({'start_th1': start_block.reset_index().frame,
                             'end_th1': end_block.reset_index().frame})
    # extend block based on th_2
    block_df['end_th2'] = np.nan
    block_df['start_th2'] = np.nan
    for i, row in block_df.iterrows():
        point_below_th2 = treshold_df.loc[:row.start_th1,
                                          'th_2'].dropna()
        # check if a point is below th2
        if len(point_below_th2) > 0:
            start_th2 = point_below_th2.index[-1]
        else:
            start_th2 = row.start_th1
        # Check if the point is before th1
        if start_th2 <= row.start_th1:
            block_df.loc[i, 'start_th2'] = start_th2

        point_below_th2 = treshold_df.loc[row.start_th1:, 'th_2'].dropna()
        # check if a point is below th2
        if len(point_below_th2) > 0:
            end_th2 = point_below_th2.index[0]
        else:
            end_th2 = row.end_th1
        # Check if the point is after th1
        if end_th2 >= row.end_th1:
            block_df.loc[i, 'end_th2'] = end_th2

    return block_df


def extract_block_nonans(data):
    return extract_block(data.isnull() == 0, thresholds=[0.4, 0.5])
