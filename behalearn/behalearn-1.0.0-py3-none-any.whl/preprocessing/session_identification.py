import pandas as pd


def timespan_threshold(time, threshold=None):
    """
    function to identify if current event belongs to same session

    :param time:
    :param threshold: time between 2 events in one session can not be
                    greater than set threshold (on default it is set to
                    30 minutes)
    :return: boolean if time is null or if time is greater than set threshold
            (true - new session, false - same session )
    """

    if threshold is None:
        threshold = pd.Timedelta(minutes=30)
    return pd.isnull(time) or time > threshold


def session_ids(data, threshold_func, **kwargs):
    """
    function to identify session ids for all events for multiple users with
    unique ids

    :param data: difference between 2 events, all events are sorted by
                user id and event time (in this order)
    :param threshold_func: function to detect threshold (new session when
                          function return True)
    :return: array of detected session ids
    """

    session_act = 0
    session_ids = []

    for row in data:
        if threshold_func(row, **kwargs):
            session_act += 1
        session_ids.append(session_act)

    return session_ids
