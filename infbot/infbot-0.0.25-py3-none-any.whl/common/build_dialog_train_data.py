
import numpy as np
from sklearn.utils import shuffle
from infbot.logger import logger


def make_new_state(state, domain, intent, slots, utterance='', reset_slots=[]):
    new_state = state.clone()
    new_state.user_domain = domain
    new_state.user_intent = intent
    new_state.utterance = utterance
    filled = []
    for slot in slots:
        if isinstance(slot, str):
            slot_name = slot
            value = 1
        else:
            slot_name = slot['slot_name']
            value = slot['slot_value']
        if intent.startswith('request'):
            stype = 'requestable'
        else:
            stype = 'informable'
        filled.append(slot_name)
        new_state[(stype, slot_name)] = value
    for slot in new_state.slots:
        if slot['type'] == 'informable' and slot['name'] in reset_slots \
                and slot['name'] not in filled:
            slot['value'] = None
        elif slot['type'] == 'requestable' \
                and slot['name'] not in filled:
            slot['value'] = None
    return new_state


def build_dialog_train_data(dialogs, init_state, n_history=6, n_times=50):
    x_dst, y_dst = [], []
    x_dpl, y_dpl = [], []
    history = []
    for i in range(n_history):
        history.append(init_state.clone())

    for i_times in range(n_times):
        if i_times > 0:
            dialogs = shuffle(dialogs)
        for dialog in dialogs:
            for turn in dialog:
                state = history[-1].clone()  # last history
                if 'user' in turn:
                    new_state = make_new_state(
                        init_state,
                        turn['domain'],
                        turn['intent'],
                        turn['slots'],
                        reset_slots=turn['reset_slots']
                    )

                    slot_vec = state.slot_vec
                    new_slot_vec = new_state.slot_vec
                    y = np.array([
                        1 if a != b else 0
                        for a, b in zip(
                            slot_vec.tolist(), new_slot_vec.tolist())
                    ])

                    x = np.concatenate([
                        s.vec
                        for s in history
                    ] + [new_state.vec])
                    x_dst.append(x)
                    y_dst.append(y)
                    history = history[1:] + [new_state]
                if 'sys' in turn:
                    x = np.concatenate([s.vec for s in history])
                    state.sys_intent = turn['intent']
                    y = state.sys_vec
                    x_dpl.append(x)
                    y_dpl.append(y)

    x_dst = np.array(x_dst)
    y_dst = np.array(y_dst)
    x_dpl = np.array(x_dpl)
    y_dpl = np.array(y_dpl)
    logger.info(
        'dialog train data, x_dst %s y_dst %s x_dpl %s y_dpl %s',
        x_dst.shape, y_dst.shape, x_dpl.shape, y_dpl.shape)
    return x_dst, y_dst, x_dpl, y_dpl
