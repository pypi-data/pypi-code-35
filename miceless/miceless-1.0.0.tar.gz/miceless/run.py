#!/usr/bin/python3
import logging
import os
from pynput import keyboard

from miceless.state import StateTracker


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler()])
    state = StateTracker(os.path.join(os.getenv('HOME'), '.miceless'))

    with keyboard.Listener(
            on_press=state.pressed,
            on_release=state.released) as listener:
        listener.join()
