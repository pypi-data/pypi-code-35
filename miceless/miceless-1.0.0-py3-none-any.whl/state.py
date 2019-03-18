import json
import logging
from pynput import keyboard, mouse
from time import sleep


class StateTracker:
    def __init__(self, config_path):
        self._config_path = config_path
        self._logger = logging.getLogger(__name__)
        self._is_r_alt = False
        self._is_r_ctrl = False
        self._is_rec_mode = False
        self._mouse = mouse.Controller()
        self._memory = {}
        self.load()
        self._last_key = None
        for k, v in self._memory.items():
            self._logger.info(f'Loaded bind {k} = {v}')
        self._logger.info(f'Initialized in {"REC" if self._is_rec_mode else "PLAY"}')

    def check_modifiers(self):
        return self._is_r_alt and self._is_r_ctrl

    def dump(self):
        with open(self._config_path, 'w') as f:
            json.dump(self._memory, f)

    def load(self):
        try:
            with open(self._config_path, 'r') as f:
                self._memory = json.load(f)
            self._logger.info(f'Loaded {self._config_path}')
        except FileNotFoundError:
            self._logger.info('Nothing to load')

    @staticmethod
    def is_key_allowed(key):
        return len(str(key)) == 3

    def pressed(self, key):
        if key == keyboard.Key.alt_r:
            self.set_r_alt(True)
        elif key == keyboard.Key.ctrl_r:
            self.set_r_ctrl(True)

    def released(self, key):
        if key == keyboard.Key.alt_r:
            self.set_r_alt(False)
        elif key == keyboard.Key.ctrl_r:
            self.set_r_ctrl(False)
        if self.check_modifiers() and self.is_key_allowed(key):
            if key == keyboard.KeyCode.from_char(char='`'):
                # Toggle mode.
                self._is_rec_mode = not self._is_rec_mode
                self._logger.info(f'Mode set to {"REC" if self._is_rec_mode else "PLAY"}')
            elif self._is_rec_mode:
                if key == keyboard.KeyCode.from_char(char='0'):
                    if self._last_key.char in self._memory:
                        del self._memory[self._last_key.char]
                        self.dump()
                        self._logger.info(f'Cleared key {self._last_key}')
                else:
                    if key.char not in self._memory:
                        self._memory[key.char] = []
                    self._memory[key.char].append(self._mouse.position)
                    self.dump()
                    self._logger.info(f'Recorded position {self._memory[key.char]} for key {key}')
            elif key.char in self._memory:
                self._logger.info(f'Executing {len(self._memory)} actions for key {key}')
                for pos in self._memory[key.char]:
                    self._mouse.position = pos
                    self._mouse.click(mouse.Button.left)
                    self._logger.info(f'Clicked: {pos}')
                    sleep(0.2)
            self._last_key = key

    def set_r_alt(self, state):
        self._is_r_alt = state

    def set_r_ctrl(self, state):
        self._is_r_ctrl = state
