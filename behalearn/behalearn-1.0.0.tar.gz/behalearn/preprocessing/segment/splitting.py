import numpy as np


def split(data, criteria):
    """
    Function that returns labels defining segments in dataframe according to
    criteria

    :param data: DataFrame containing all required fields for splitting
    :param criteria: Tuple of tuples containing function reference and its\
            argument list
    :return: List of labels defining segment
    """

    segment_ends = []
    offset = 0
    while offset <= data.shape[0] - 1:
        segment_end = data.shape[0] - 1
        for func, kwargs in criteria:
            curr_segment_end = func(data, offset, **kwargs)
            if curr_segment_end < segment_end:
                segment_end = curr_segment_end
        segment_ends.append(segment_end)
        offset = segment_end + 1

    seg_start = 0
    seg_label = 0
    segments_labels = []
    for segment_end in segment_ends:
        segments_labels += [seg_label for _ in
                            range(seg_start, segment_end + 1)]
        seg_start = segment_end + 1
        seg_label += 1
    return segments_labels


def criteria_by_time_interval(data, offset, time_interval):
    """
    Returns index of last element in segment (segment starts at offset in data)
    defined by time interval in which events of segment occured.

    :param data: Dataframe containing sorted time column
    :param offset: Index in data where segment starts
    :param time_interval: Time value in same units as data
    :return: Index of last element in segment
    """
    data = data['time']
    time_start = data.values[offset]
    for index, row in enumerate(data.values[offset:]):
        if row - time_start > time_interval:
            return index + offset - 1

    return data.shape[0] - 1


def criteria_by_silence_time(data, offset, silence_time):
    """
    Returns index of last element in segment
    (Segment that starts at offset in data)
    defined by silence time between 2 events.

    :param data: Dataframe containing sorted time column
    :param offset: Index in data where segment starts
    :param silence_time: Time value in same units as data
    :return: Index of last element in segment
    """
    if data.shape[0] == offset + 1:
        return offset

    data = data['time']
    prev_row = data.values[offset]
    for index, row in enumerate(data.values[offset + 1:]):
        if row - prev_row >= silence_time:
            return index + (offset + 1) - 1
        prev_row = row

    return data.shape[0] - 1


def split_segment(segment, s_counts):
    """
    Function that returns labels of segment split defined by percentual
    proportion or by count in each subsegment

    :param segment: array of segment ids containing at least length of
                    s_counts array
    :param s_counts: array which sum of elements has to be 100
                    (when indicating percentual delimeters) or
                    length of segment array
    :return: list of segment ids after splitting
    """
    s_counts = np.array(s_counts)
    segment = np.array(segment)

    if s_counts.sum() == 100:
        s_counts = (s_counts / 100) * segment.shape[0]
        s_counts = np.rint(s_counts).astype(int)
        if s_counts.sum() != segment.shape[0]:
            s_counts[-1] += segment.shape[0] - s_counts.sum()

    result = []
    seg_index = 0
    for seg_len in s_counts:
        result += [seg_index for _ in range(seg_len)]
        seg_index += 1

    return result
