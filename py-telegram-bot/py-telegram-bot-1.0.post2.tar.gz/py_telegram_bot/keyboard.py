import json


class ReplyKeyboardButton:
    def __init__(self, text):
        self.text = text


class InlineKeyboardButton:
    def __init__(self, text, **kwargs):
        self.text = text
        self.kwargs = kwargs
        if text not in kwargs:
            kwargs.update({'text': text})


class ReplyKeyboard:
    def __init__(self, resize_keyboard: bool = True, one_time_keyboard: bool = False):
        self.keyboard = [[]]
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard

    def add_button(self, button: (ReplyKeyboardButton, str)):
        if isinstance(button, str):
            self.keyboard[-1].append(button)
        else:
            self.keyboard[-1].append(button.text)

    def add_line(self):
        self.keyboard.append([])

    def current_line_size(self):
        return len(self.keyboard[-1])

    def get_keyboard(self):
        keyboard = {'keyboard': self.keyboard,
                    'resize_keyboard': self.resize_keyboard,
                    'one_time_keyboard': self.one_time_keyboard}
        return json.dumps(keyboard)


class InlineKeyboard:
    def __init__(self):
        self.keyboard = [[]]

    def add_button(self, button: (InlineKeyboardButton, str)):
        if isinstance(button, str):
            self.keyboard[-1].append([button])
        else:
            self.keyboard[-1].append(button.kwargs)

    def add_line(self):
        self.keyboard.append([])

    def current_line_size(self):
        return len(self.keyboard[-1])

    def get_keyboard(self):
        return json.dumps({'inline_keyboard': self.keyboard})
