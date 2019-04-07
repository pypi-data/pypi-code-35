import sys, math


class LoadingBar:

    SPACES = 70.0

    max_count = 0
    count = 0
    show_bar_after = False

    message = f'Processing Jobs'

    stdscr = None

    CURSOR_UP = '\033[F'
    ERASE_LINE = '\033[K'

    def __init__(self, max_count, message=None, show_bar_after=False):
        self.show_bar_after = show_bar_after
        self.start(max_count, message)

    def start(self, max_count, message=None):
        self.count = 0
        self.max_count = int(max_count)
        if message is not None:
            self.message = message
        sys.stdout.write(self.message + '\n')

    def add_count(self, job_string=None):
        self.count += 1
        if self.count > 1:
            self._remove_stdout_lines(2)
        if self.count >= self.max_count:
            self._remove_stdout_lines(1)
            sys.stdout.write(self.message + '...Done \n')
            if self.show_bar_after:
                self._write_loading_bar(job_string)
            return True
        self._write_loading_bar(job_string)
        return False

    def _remove_stdout_lines(self, number):
        for x in range(number):
            sys.stdout.write(self.CURSOR_UP + self.ERASE_LINE)

    def _write_loading_bar(self, job_string=None):
        sys.stdout.write(f'[{self._get_inner_string()}] {self._rounded_percentage()}% \n' +
                         f'processed job {self.count}/{self.max_count}' +
                         (f': {job_string}' if job_string is not None else '...') +
                         f' \n')

    def _real_percentage(self):
        if self.count == 0:
            return 0
        return self.count / (self.max_count / 100)

    def _rounded_percentage(self):
        return round(self._real_percentage(), 1)

    def _spacial_count(self):
        return (self.SPACES / 100) * self._real_percentage()

    def _ceil_count(self):
        return math.ceil(self._spacial_count())

    def _get_inner_string(self):
        ceil = self._ceil_count()
        if ceil == int(self.SPACES):
            return '=' * int(self.SPACES)
        elif ceil == 0:
            return ' ' * int(self.SPACES)
        equals = ceil - 1
        spaces = int(self.SPACES) - int(equals) - 1
        return ('=' * int(equals)) + '>' + (' ' * int(spaces))
