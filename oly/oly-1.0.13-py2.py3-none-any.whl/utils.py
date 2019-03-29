import os
import shutil
import json
import sys
import click


class Utils:
    def __init__(self):
        pass

    BASE_NAME = 'oly-cli'
    HOME = os.getenv('HOME')
    OLY_HOME = os.path.join(HOME, '.oly')
    ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    LIBS_DIR = os.path.abspath(os.path.dirname(__file__))
    CONFIG_FILE = os.path.join(OLY_HOME, 'config.json')
    TOOLS_DIR = os.path.join(OLY_HOME, 'tools')
    PROJECTS_DIR = os.path.join(HOME, 'oly-projects')
    SERVICES_PREFIX = 'oly_'
    NETWORK = 'olynet'
    VERSION = open(os.path.join(LIBS_DIR, 'version.txt')).read().strip()

    @staticmethod
    def is_json(my_json):
        try:
            json.loads(my_json)
        except ValueError:
            return False
        return True

    @staticmethod
    def cli_obfuscate(txt):
        t_len = len(txt)
        return '*' * t_len

    @staticmethod
    def m_input(txt):
        py_version = sys.version_info[:2]
        if py_version <= (2, 7):
            return raw_input(txt)
        return input(txt)

    def input_with_help(self, question, prompt, *answers):
        print(question)
        for i, answer in enumerate(answers, 1):
            # print('  ' + str(i), '-', Clr.OK + answer + Clr.RESET)
            click.echo('  ' + str(i) + ' - ' + click.style(answer, fg='green'))

        print
        return self.m_input(prompt)

    @staticmethod
    def empty_dir(mdir):
        for the_file in os.listdir(mdir):
            file_path = os.path.join(mdir, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(e)

def merge(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z


class Clr:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    OK = '\033[32m'
    WARNING = '\033[33m'
    FAIL = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    MARK_ERROR = '\033[41m'
    MARK_OK = '\033[42m'

    def __init__(self, message):
        self.message = message

    def ok(self):
        print(self.OK + self.message + self.RESET)

    def ok_banner(self):
        text = '%s%s%s' % (' ', self.message, ' ')
        test_len = len(text)
        print(self.MARK_OK + ' ' * test_len + self.RESET)
        print(self.MARK_OK + text + self.RESET)
        print(self.MARK_OK + ' ' * test_len + self.RESET)

    def head(self):
        print(self.HEADER + self.message + self.RESET)

    def fail(self):
        print(self.FAIL + self.message + self.RESET)

    def warn(self):
        print(self.WARNING + self.message + self.RESET)

    def blue(self):
        print(self.BLUE + self.message + self.RESET)

    def error(self, msg_prefix='Error: '):
        print(self.FAIL + msg_prefix + self.RESET + self.message)

    def error_banner(self):
        click.echo()
        max_len = 0
        text = ''
        if '\n' in self.message:
            stext = str(self.message).strip().split('\n')

            # get the string length
            for line in stext:
                if len(line.strip()) > max_len:
                    max_len = len(line.strip())

            for line in stext:
                r_blank = (max_len - len(line.strip()))
                blank = ' ' * r_blank
                text += '%s%s%s' % (self.MARK_ERROR + ' ', line.strip(), blank + ' ' + self.RESET + '\n')
        else:
            text = '%s%s%s' % (self.MARK_ERROR + ' ', self.message, ' ' + self.RESET)
            max_len = len(self.message.strip())

        print(self.MARK_ERROR + ' ' * (max_len + 2) + self.RESET)
        print(text.rstrip('\n'))
        print(self.MARK_ERROR + ' ' * (max_len + 2) + self.RESET)
        click.echo()

    def fatal(self):
        self.error('Fatal: ')
        exit(1)
