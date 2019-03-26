import json
import pandas as pd


def _process_row(row, state):
    """
    Returns list of series, where each represents separate touch pointer
     with touch event information

    :param row: Series row containing event_type and list of touches in
    payload_touches column
    :param state:
    :return:
    """
    row = row.to_dict()
    event_type = row['event_type']
    touches = json.loads(row['payload_touches'].replace('\'', '"'))

    if len(state) == 0:
        state.extend(touches)
        return [{**row, **touches[0]}]

    res = []
    if event_type == 'TOUCH_START':
        touch_mapped = {}
        for touch in touches:
            if touch not in state:
                state.append(touch)
                touch_mapped.update(touch)
        res.append({**row, **touch_mapped})

    if event_type in ['TOUCH_END', 'TOUCH_CANCEL']:
        touch_mapped = {}
        ended_touches = []

        for touch in state:
            if touch not in touches:
                ended_touches.append(touch)
                touch_mapped.update(touch)
        res.append({**row, **touch_mapped})

        for touch in ended_touches:
            state.remove(touch)

    if event_type == 'TOUCH_MOVE':
        for touch in touches:
            if touch not in state:
                res.append({**row, **touch})
        state.clear()
        state.extend(touches)

    return res


def flat_touches(data):
    """
    Function return DataFrame with flat touches from payload_touches column.
    Each touch is transformed to separate row.

    :param data: DataFrame containing touch events
    :return: DataFrame containing separate row for each touch pointer and
    touch event information
    """
    state = []
    processed_rows = []
    for i, row in data.iterrows():
        processed_rows.extend(_process_row(row, state))

    result = pd.DataFrame(processed_rows).drop(
        columns='payload_touches',
        errors='ignore'
    )

    renaming_map = {
        'positionX': 'position_x',
        'positionY': 'position_y'
    }

    return result.rename(columns=renaming_map)
