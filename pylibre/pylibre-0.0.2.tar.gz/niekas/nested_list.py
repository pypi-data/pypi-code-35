from typing import List, Optional
import readchar
import logging
import re
import os
import subprocess


logging.basicConfig(filename='logs.txt', filemode='a', datefmt='%H:%M:%S', level=logging.DEBUG,
                    format='%(asctime)s %(message)s')


class Note:
    def __init__(self, text):
        self.children = []
        self.parent = None
        self.text = text

        # What is the next step? Very long line - Note should return a bunc.
        #  Sprendimas: spausdinimas gana puikiai veikia, tik reikia
        #  išsisaugoti, kiek kiekvienas elemenas užima vietos.


        #
        # Data structure which is loaded and provides the abstraction for printing a fragment

        # Nurodžius kursoriaus poziciją.
        #
        #   Nurodžius eilutės ilgį grąžinti žinutės fragmentą.
        #   Kaip kursoriaus pozicija susijusi su rodomu fragmentu?
        #       Jeigu 10% pločio peržengia, tada paslinkti.
        #       Jeigu į vieną pusę arba į kitą peržengia, tada paslinkti vaizdą.


    def show(self):
        pass

    def level(self):
        levels = 0
        parent = self.parent
        while parent is not None:
            levels += 1
            parent = parent.parent
        return levels




class NestedList:
    def __init__(self, filename='my_list.txt'):
        self.rows = 0
        self.filename = filename
        self.my_list = self.load_list()
        self.mode = 'command'
        self.prefix = '[ ] '
        self.pos = [0, len(self.prefix)]  # Coordinates in the monitor
        self.keypress = None
        self.logger = logging.getLogger('NestedList')

    @property
    def row(self): # Cursor row
        return self.pos[0]

    @property
    def col(self): # Cursor column
        return self.pos[1] - len(self.prefix)

    @col.setter
    def col(self, value):
        self.pos[1] = value + len(self.prefix)


    def load_list(self):
        my_list = []
        for line in open(self.filename):
            my_list.append(Note(line.strip()))
        return my_list

    def clear(self):
        print(''.join(['\033[K\n']*(self.rows)), flush=True)
        # print(f'\033[{len(self.my_list)}A', end='', flush=True)
        print('\033[H', end='', flush=True)  # TODO: use \033[K to clear screan
        # print('\033[2J\033[H', end='', flush=True)  # TODO: use \033[K to clear screan
        # print('\033[2J\033[H', end='', flush=True)  # TODO: use \033[K to clear screan

    def update_cursor_pos(self):
        if self.keypress in ['j', 'J', readchar.key.DOWN]:
            self.pos[0] = self.pos[0] + 1 if self.pos[0] + 1 <= self.rows else self.pos[0]
        elif self.keypress in ['k', 'K', readchar.key.UP]:
            self.pos[0] = self.pos[0] - 1 if self.pos[0] > 0 else 0
        elif self.keypress in ['l', 'L', readchar.key.RIGHT]:
            self.pos[1] = self.pos[1] + 1
        elif self.keypress in ['h', 'H', readchar.key.LEFT]:
            self.pos[1] = self.pos[1] - 1 if self.pos[1] > 0 else 0

    #
    # $, space, o >> <<
    # e b dw D
    #

    def save_list(self):
        with open(self.filename, 'w') as f:
            for note in self.my_list:
                f.write('    ' * note.level() + note.text + '\n')
            # f.write('\n'.join(self.my_list))

    def show_list(self):
        # lines, columns = subprocess.check_output('echo $LINES $COLUMNS', shell=True).decode().strip().split()
        lines, columns = os.popen('stty size', 'r').read().split()
        self.terminal_lines = int(lines)
        self.terminal_columns = int(columns)
        for note in self.my_list:
            note.from_row = self.rows
            self.rows += (len(self.prefix) + len(note.text)) // self.terminal_columns
            note.to_row = self.rows
            print(f'\033[K{self.prefix}{note.text}')
        print(f'\033[{self.rows + 1}A', end='', flush=True)

    def move_cursor(self):
        if self.pos[0]:
            print(f'\033[{self.pos[0]}B', end='', flush=True)
        if self.pos[1]:
            print(f'\033[{self.pos[1]}C', end='', flush=True)

    def show(self):
        print('\033[2J\033[H', end='', flush=True)
        while True:
            self.clear()
            self.show_list()
            self.move_cursor()
            self.keypress = readchar.readchar()

            self.logger.info(f'Key pressed {self.keypress} ({ord(self.keypress[0])}) ')
            if self.keypress in [readchar.key.CTRL_C, readchar.key.CTRL_D]:
                break
            elif self.mode == 'command':
                if self.keypress in 'jJkKlLhH':
                    self.update_cursor_pos()
                elif self.keypress == 'i':
                    self.mode = 'insert'
                elif self.keypress == 'o':
                    self.pos[0] += 1
                    self.pos[1] = len(self.prefix)
                    self.my_list.insert(self.pos[0], '')
                    self.mode = 'insert'
                elif self.keypress == 'a':
                    self.pos[1] += 1
                    self.mode = 'insert'
                elif self.keypress == 'w':
                    try:
                        s = self.my_list[self.pos[0]].text[self.pos[1] - len(self.prefix):]
                        i = 0
                        if re.search(r'\s\w', s):
                            i = re.search(r'\s\w', s).start() + 1
                        self.pos[1] = i + self.pos[1]
                    except ValueError:
                        self.pos[1] = self.pos[1]
                elif self.keypress == 'b':
                    s = self.my_list[self.row].text[:self.col][::-1]
                    i = 0
                    if re.search(r'(?!^\s)\s\S', s):
                        i = re.search(r'(?!^\s)\s\S', s).start()
                        self.col = self.col - i if self.col >= i else 0
                    else:
                        self.col = 0
                elif self.keypress == 'e':
                    s = self.my_list[self.row].text[self.col:]
                    i = 0
                    if re.search(r'(?!^\S)\S\s', s):
                        i = re.search(r'(?!^\S)\S\s', s).start()
                        self.logger.info(f'i={i}, s="{s}"')
                        self.col = self.col + i
                    else:
                        self.col = self.rows - 1
                elif self.keypress == '$':
                    self.col = len(self.my_list[self.row]) - 1
                elif self.keypress == ' ':
                    self.col = 0
                elif self.keypress == '>': # TODO:
                    self.keypress = readchar.readchar()
                    if self.keypress == '>':
                        pass
                elif self.keypress == '<':
                    self.keypress = readchar.readchar()
                    if self.keypress == '<':
                        pass
                elif self.keypress == 'O':
                    self.pos[1] = len(self.prefix)
                    self.my_list.insert(self.pos[0], '')
                    self.mode = 'insert'
                elif self.keypress == ':':
                    self.keypress = readchar.readchar()
                    self.logger.info('Key pressed after : ' + self.keypress)
                    if self.keypress == 'q':
                        self.keypress = readchar.readchar()
                        break
                    elif self.keypress == 'w':
                        self.save_list()
                        self.keypress = readchar.readchar()
                        if self.keypress == 'q':
                            self.keypress = readchar.readchar()
                            break

            elif self.mode == 'insert':
                if self.keypress == readchar.key.ESC:
                    self.mode = 'command'
                else:
                    s = self.my_list[self.pos[0]].text
                    p = self.pos[1] - len(self.prefix)
                    if self.keypress == readchar.key.BACKSPACE:
                        self.my_list[self.pos[0]].text = s[:p -1] + s[p:]
                        self.pos[1] = self.pos[1] - 1 if self.pos[1] > 0 else 0
                    else:
                        self.my_list[self.pos[0]].text = s[:p] + self.keypress + s[p:]
                        self.pos[1] += 1


        print('\033[2J\033[H', end='', flush=True)
        # print('\033[K\n\033[K\n\033[K\n\033[3A')


# \033[2J      Clear the screen.
# \033[H       Move the cursor to the upper-left corner of the screen.
# \033[r;cH    Move the cursor to row r, column c. Note that both the rows and columns are indexed starting at 1.
# \033[?25l    Hide the cursor.
# \033[K       Delete everything from the cursor to the end of the line.
# \033[<N>A    Move the cursor up N lines.
# \033[<N>B    Move the cursor down N lines.
# \033[<N>C    Move the cursor forward N columns.
# \033[<N>D    Move the cursor backward N columns.



def prompt_yes_or_no(
        question: str,
        yes_text: str = 'Yes',
        no_text: str = 'No',
        has_to_match_case: bool = False,
        enter_empty_confirms: bool = True,
        default_is_yes: bool = False,
        deselected_prefix: str = '  ',
        selected_prefix: str = '\033[31m>\033[0m ',
        abort_value: Optional[bool] = None,
        char_prompt: bool = True) -> Optional[bool]:
    """Prompt the user to input yes or no.

    Args:
        question (str): The prompt asking the user to input.
        yes_text (str, optional): The text corresponding to 'yes'.
        no_text (str, optional): The text corresponding to 'no'.
        has_to_match_case (bool, optional): Does the case have to match.
        enter_empty_confirms (bool, optional): Does enter on empty string work.
        default_is_yes (bool, optional): Is yes selected by default (no).
        deselected_prefix (str, optional): Prefix if something is deselected.
        selected_prefix (str, optional): Prefix if something is selected (> )
        abort_value (bool, optional): The value to return on interrupt.
        char_prompt (bool, optional): Add a [Y/N] to the prompt.

    Returns:
        Optional[bool]: The bool what has been selected.
    """
    is_yes = default_is_yes
    is_selected = enter_empty_confirms
    current_message = ''
    yn_prompt = f' ({yes_text[0]}/{no_text[0]}) ' if char_prompt else ': '
    abort = False
    print()
    while True:
        yes = is_yes and is_selected
        no = not is_yes and is_selected
        print('\033[K'
              f'{selected_prefix if yes else deselected_prefix}{yes_text}')
        print('\033[K'
              f'{selected_prefix if no else deselected_prefix}{no_text}')
        print('\033[3A\r\033[K'
              f'{question}{yn_prompt}{current_message}', end='', flush=True)
        keypress = readchar.readkey()
        if keypress in [readchar.key.DOWN, readchar.key.UP]:
            is_yes = not is_yes
            is_selected = True
            current_message = yes_text if is_yes else no_text
        elif keypress in [readchar.key.BACKSPACE, readchar.key.LEFT]:
            if current_message:
                current_message = current_message[:-1]
        elif keypress in [readchar.key.CTRL_C, readchar.key.CTRL_D]:
            abort = True
            break
        elif keypress in [readchar.key.ENTER, readchar.key.RIGHT]:
            if is_selected:
                break
        elif keypress == readchar.key.ESC:
            if is_selected:
                current_message = yes_text if is_yes else no_text
        else:
            current_message += keypress
            match_yes = yes_text
            match_no = no_text
            match_text = current_message
            if not has_to_match_case:
                match_yes = match_yes.upper()
                match_no = match_no.upper()
                match_text = match_text.upper()
            if match_no.startswith(match_text):
                is_selected = True
                is_yes = False
            elif match_yes.startswith(match_text):
                is_selected = True
                is_yes = True
            else:
                is_selected = False
        print()
    print('\033[K\n\033[K\n\033[K\n\033[3A')
    if abort:
        return abort_value
    return is_selected and is_yes





if __name__ == '__main__':
    NestedList().show()
