class Stack:
    """
    A simple stack with some additional functionality that supports command-line
    parsing. A stack provides an intuitive way to parse the command line.
    """
    def __init__(self, items):
        """
        Initializes the stack from the passed List such that the left-most list
        item is the top of the stack, and the right-most list item is the bottom of the
        stack

        :param items: the List to initialize the stack from. If None, then the stack
        is initialized to be empty
        """
        self._items = []
        self._items.extend(reversed(items if items else []))

    def __repr__(self):
        return str([item for item in reversed(self._items)])

    def is_empty(self):
        return self._items == []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        return self._items.pop()

    def peek(self):
        return self._items[len(self._items) - 1]

    def size(self):
        return len(self._items)

    def pop_all(self):
        to_return = list(reversed(self._items))
        self._items = []
        return to_return

    def has_options(self):
        """
        Checks to see if the stack contains any more options (i.e.
        tokens that start with dash or double dash.)

        :return: True if the stack contains any more options, else False
        """
        remaining_opts = [item for item in self._items if item.startswith("-")]
        return len(remaining_opts) != 0
