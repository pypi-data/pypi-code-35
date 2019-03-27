# -*- coding:utf-8 -*-
import os
from sicfw.sicfw import Mode, set_global, get_global, start

MEMO = os.path.expanduser('~/.global_memo_v0_0_1')
GLOBAL_INPUT = 'input_lines'
GLOBAL_LINENUM = 'line_num'

class InitialMode(Mode):

    def wait_command(self):
        return 'init'

    @Mode.command('init')
    def initialize(self):
        if os.path.exists(MEMO):
            lines = []
            with open(MEMO, 'r') as f:
                for line in f:
                    lines.append(line.strip())
            set_global(GLOBAL_INPUT, lines)
        else:
            set_global(GLOBAL_INPUT, [])

        return MemoMode

    @Mode.after_command_message('init')
    def initial_message(self):
        return get_global(GLOBAL_INPUT)

class MemoMode(Mode):

    @Mode.after_command_message('--help')
    def help(self):
        message = ['Commands:',
                   '-q        : Quit gmemo.',
                   '-s --save : Save curret memo.',
                   '--replace : Replace line.',
                   '--reset   : Initialize memo.',
        ]
        return message

    @Mode.command('-q')
    def quit_command(self):
        exit(0)

    @Mode.command('--read')
    def read_command(self):
        if os.path.exists(MEMO):
            lines = []
            with open(MEMO, 'r') as f:
                for line in f:
                    lines.append(line.strip())
            set_global(GLOBAL_INPUT, lines)
        return MemoMode

    @Mode.after_command_message('--read')
    def after_read_message(self):
        message = ['----------------',
                   'read succeeded!!',
                   '----------------'
        ]
        lines = get_global(GLOBAL_INPUT)
        message.extend(lines)
        return message

    @Mode.command(('-s', '--save'))
    def save_command(self):
        lines = get_global(GLOBAL_INPUT)
        with open(MEMO, 'w') as f:
            for l in lines:
                f.write(l + '\n')
        return MemoMode

    @Mode.after_command_message(('-s', '--save'))
    def after_save_message(self):
        message = ['----------------',
                   'save succeeded!!',
                   '----------------'
        ]
        return message

    @Mode.free_input
    def free(self, command):
        lines = get_global(GLOBAL_INPUT)
        if lines:
            lines.append(command)
        else:
            lines = [command]
        set_global(GLOBAL_INPUT, lines)
        return MemoMode

    @Mode.command('--replace')
    def change2replace_mode(self):
        return ReplaceMode1

    @Mode.command(('-r', '--reset'))
    def reset(self):
        set_global(GLOBAL_INPUT, [])
        return MemoMode

class ReplaceMode1(Mode):

    def premessage(self):
        message = ['------------------------------',
                   'input line number for replace.',
                   '------------------------------'
        ]
        lines = get_global(GLOBAL_INPUT)
        lines = ['{:>3}'.format(line_num + 1) + ' | ' + line
                  for line_num, line in enumerate(lines)]
        message.extend(lines)
        return message

    @Mode.free_input
    def select_line(self, command):
        try:
            line_number = int(command)
        except:
            return ReplaceMode1

        lines = get_global(GLOBAL_INPUT)
        if line_number > 0 and line_number <= len(lines):
            set_global(GLOBAL_LINENUM, line_number)
            return ReplaceMode2
        else:
            return ReplaceMode1


class ReplaceMode2(Mode):

    def premessage(self):
        lines = get_global(GLOBAL_INPUT)
        line_num = get_global(GLOBAL_LINENUM)
        message = ['-------------------',
                   'replace target line',
                   '-------------------',
                   lines[line_num - 1]
        ]
        return message

    @Mode.free_input
    def replace_line(self, command):
        lines = get_global(GLOBAL_INPUT)
        line_num = get_global(GLOBAL_LINENUM)
        lines[line_num - 1] = command
        set_global(GLOBAL_INPUT, lines)
        return MemoMode

    @Mode.after_free_input_message
    def after_message(self, command):
        lines = get_global(GLOBAL_INPUT)
        message = ['-------------------',
                   'replace succeeded!!',
                   '-------------------'
        ]
        message.extend(lines)
        return message

def main():
    start(InitialMode)

if __name__ == '__main__':
    main()