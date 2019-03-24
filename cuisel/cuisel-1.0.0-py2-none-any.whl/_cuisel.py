import curses
from cuisel.controller import VIMController
from cuisel.viewer import VIMViewer

def cuisel(items, title=None, number=False, modeline=True):
    """
    This is a command-line user interface which helps you select
    from a list of items.

    @param items: a list of candidates
    @param title: a title which will be displayed at the top the screen
    @param number: turns on/off line numbers
    @param modeline: turns on/off modeline
    """

    if not isinstance(items, list):
        raise TypeError('items must be a list, not \'{}\''.format(type(items)))
    if not items:
        return []

    nitems = len(items)
    flags = set()

    def _select(wnd):
        wndh, wndw = wnd.getmaxyx()

        reserved_height = 0
        if title:
            reserved_height += 2
        if modeline:
            reserved_height += 2
        ctl = VIMController(nitems, height=min([wndh-reserved_height, nitems]))
        viewer = VIMViewer(wnd, title=title, number=number,
                modeline=modeline)

        while True:
            viewer.draw(items, flags, ctl)
            # handle input
            key = wnd.getch()
            if key == ord('q'):
                break
            ctl.handle_key(key, flags)

    curses.wrapper(_select)

    return [(i, items[i]) for i in range(nitems) if i in flags]

