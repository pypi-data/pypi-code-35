from threading import Lock
from threading import Timer as TimerThread


class Frame:
    def __init__(self):
        self._frames = []

    def __getitem__(self, idx: int):
        return self._frames[idx]

    def __iter__(self):
        return iter(self.frames)

    def __str__(self):
        return str({"size": len(self._frames), "frames": self._frames})

    def __len__(self):
        return len(self._frames)

    @property
    def frames(self):
        return self._frames.copy()

    @property
    def size(self):
        return len(self._frames)


class Fixed(Frame):
    def __init__(self, maxsize):
        self._maxsize = maxsize
        self._lock = Lock()
        super().__init__()

    @property
    def is_full(self):
        """ Returns True if number of items are equal to the size limit

        Returns
        -------
        bool
            True if number of items are equal to the size limit
        """
        with self._lock:
            return True if self._maxsize <= len(self._frames) else False

    @property
    def maxsize(self):
        with self._lock:
            return self._maxsize

    @maxsize.setter
    def maxsize(self, maxsize):
        with self._lock:
            if maxsize < self._maxsize and maxsize > 0:
                self._maxsize = maxsize
                self._frames = self._frames[:maxsize]

    def slide(self, item):
        """ Adds a new item

        Adding item and deletes the last item if max items

        Parameters
        ----------
        item : obj
            Any arbitrary object

        Returns
        -------
        list
            Current items
        """
        with self._lock:
            self._frames.insert(0, item)
            if len(self._frames) > self._maxsize:
                del self._frames[-1]
        return self.frames


class Timer(Frame):
    def __init__(self, interval):
        """ Timer

        Deleting data after elapsed time

        Parameters
        ----------
        interval : int
            timer interval
        """
        self._interval = interval
        super().__init__()

    def slide(self, item):
        """ Adds a new item

        Removes the item after n seconds elapsed.

        Parameters
        ----------
        item : obj
            Any arbitrary object

        Returns
        -------
        list
            Current items
        """

        self._frames.insert(0, item)
        timer = TimerThread(self._interval, self.__timeout__)
        timer.daemon = True
        timer.start()
        return self._frames

    def __timeout__(self):
        del self._frames[-1]
