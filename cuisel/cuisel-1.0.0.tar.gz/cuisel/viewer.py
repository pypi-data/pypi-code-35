import curses

class Viewer(object):

    def __init__(self, wnd, title=None, number=False):
        """
        A viewer prints the items that are currently visible to the
        user, together with some addition information if provided.

        @param wnd: ncurses window handle
        @param title: title
        @param line_numer: turns on/off line numbers
        """

        self._wnd = wnd
        self._title = title
        self._number = number

        curses.use_default_colors()
        curses.init_pair(4, 3, -1)
        self._color_batch = curses.color_pair(4)

    def draw(self, items, flags, ctl):
        """
        Prints the items, the cursor and other auxiliary information.

        @param items: the items to display
        @param flags: a set of selected indices
        @param ctl: controller
        """

        return NotImplementedError

class VIMViewer(Viewer):

    def __init__(self, wnd, title=None, number=False, modeline=True):
        super(VIMViewer, self).__init__(wnd, title=title, number=number)
        self._modeline = modeline

    def draw(self, items, flags, ctl):
        x = 0

        # title
        if self._title is not None:
            self._wnd.move(x, 0)
            self._wnd.addstr('{}'.format(self._title))
            x += 2

        number_width = len(str(len(items)))

        buf_range = ctl.get_buffer_range()
        batch_range = ctl.get_batch_range()
        for idx in range(buf_range[0], buf_range[1] + 1):
            self._wnd.move(x, 0)

            if self._number:
                self._wnd.addstr('{num: >{width}} '.format(num=idx + 1,
                    width=number_width))

            in_batch = batch_range[0] <= idx <= batch_range[1]
            selected = (idx in flags) ^ in_batch
            if selected:
                attr = curses.A_REVERSE | curses.A_BOLD
            else:
                attr = curses.A_NORMAL
            if in_batch:
                attr |= self._color_batch
            self._wnd.attron(attr)
            _, wndw = self._wnd.getmaxyx()
            width_left = wndw - number_width - 2
            self._wnd.addstr('{item: <{width}}'.format(item=items[idx][:width_left],
                width=width_left))
            self._wnd.attroff(attr)
            x += 1

        pos = ctl.get_pos()

        # a simple modeline
        if self._modeline:
            x += 1
            self._wnd.move(x, 0)
            self._wnd.addstr('selected: {num: <3} | pos: {pos: <4}'.format(
                num=len(flags), pos=pos + 1))

        x_offset = 0
        if self._title is not None:
            x_offset = 2
        if self._number:
            self._wnd.move(pos - buf_range[0] + x_offset, number_width + 1)
        else:
            self._wnd.move(pos - buf_range[0] + x_offset, 0)

