import curses

class Controller(object):
    """Handles key press events."""

    def __init__(self, nrow, height=None):
        """
        @param nrow: total number of items
        @param height: the available window height to display items, default to `nrow`
        @raise ValueError: when `nrow` or `height` is less than 1
        """

        if nrow < 1:
            raise ValueError("`nrow' must be greater than 0: {}".format(nrow))
        
        self._nrow = nrow
        self._pos = 0
        self._buffer_top = 0
        if height is None:
            self._buffer_bottom = nrow - 1
            self._height = nrow
        elif height < 1:
            raise ValueError("`height' must be greater than 0: {}".format(nrow))
        else:
            self._buffer_bottom = height - 1
            self._height = height

    def get_pos(self):
        """
        Returns the position of the cursor. It's an offset
        relative to the first item.
        """

        return self._pos

    def get_buffer_range(self):
        """Returns the range of the buffer (i.e. indices of the
        first and the last item."""

        return (self._buffer_top, self._buffer_bottom)

    def get_batch_range(self):
        """Returns the range of the batch."""

        return NotImplementedError()

    # TODO Don't pass flags directly to controller. Consider replacing
    # it with a callback?
    def handle_key(self, key, flags):
        """
        @param key: key code
        @param flags: a set of selected indices
        """
        return NotImplementedError()

class VIMController(Controller):

    def __init__(self, nrow, height=None):
        super(VIMController, self).__init__(nrow, height)
        self._count = 0
        self._batch_mode = False
        self._batch_start = -1
        self._last_key = None

    # TODO The current implementation is naive and not very flexible.
    # Try saving the key sequence and write a decent parser.
    def handle_key(self, key, flags):
        callbacks = {
            ord('j'): self.move_down,
            ord('k'): self.move_up,
            ord('g'): self.home,
            ord('G'): self.goto,
            ord('v'): self.enter_batch_mode,
            ord('u'): self.reset,
            ord('m'): self.mark,
            ord(' '): self.mark,
        }

        # gg
        if key == ord('g') and self._last_key != key:
            self._last_key = key
            return

        cb = callbacks.get(key, None)
        if cb is not None:
            self._last_key = key
            cb(flags)
            return

        self._last_key = key
        if ord('0') <= key <= ord('9'):
            if key != ord('0') or self._count:
                self._count = self._count * 10 + key - ord('0')

    def get_batch_range(self):
        if not self._batch_mode:
            return (-1, -1)
        if self._batch_start > self._pos:
            return (self._pos, self._batch_start)
        return (self._batch_start, self._pos)

    def _clear_count(clamp=True):
        """
        Reset the count to zero after handling key presses.
        @param clamp: ensures count >= 1 before moving
        """

        def decorator(cb):
            def wrapper(self, flags):
                if clamp:
                    self._count = max(1, self._count)
                cb(self, flags)
                self._count = 0
            return wrapper
        return decorator

    def _adjust_buffer(cb):
        """Adjust the buffer range when the cursor moves out of view."""

        def wrapper(self, flags):
            cb(self, flags)
            if self._pos < self._buffer_top:
                self._buffer_top = self._pos
                self._buffer_bottom = self._buffer_top + self._height - 1
            elif self._pos > self._buffer_bottom:
                self._buffer_bottom = self._pos
                self._buffer_top = self._buffer_bottom - self._height + 1
        return wrapper

    @_adjust_buffer
    @_clear_count()
    def move_down(self, flags):
        self._pos = min(self._pos + self._count, self._nrow - 1)

    @_adjust_buffer
    @_clear_count()
    def move_up(self, flags):
        self._pos = max(self._pos - self._count, 0)

    @_adjust_buffer
    @_clear_count()
    def home(self, flags):
        self._pos = max(self._count - 1, 0)

    @_adjust_buffer
    @_clear_count(clamp=False)
    def goto(self, flags):
        if self._count < 1:
            self._count = self._nrow
        self._pos = min(self._count - 1, self._nrow - 1)

    def reset(self, flags):
        if not self._batch_mode:
            flags.clear()

    @_clear_count()
    def enter_batch_mode(self, flags):
        if not self._batch_mode:
            self._batch_mode = True
            self._batch_start = self._pos

    @_clear_count()
    def mark(self, flags):
        if self._batch_mode:
            start, stop = self.get_batch_range()
        else:
            start, stop = (self._pos, self._pos)
        for row in range(start, stop + 1):
            if row in flags:
                flags.remove(row)
            else:
                flags.add(row)
        self._batch_mode = False

