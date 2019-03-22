# -*- python-indent-offset: 4; -*-

from urwid import Filler, Text, WidgetWrap


class Empty(WidgetWrap):
    def __init__(self):
        box = "┌─┐\n│ │\n└─┘"
        super().__init__(Filler(Text(box)))


class Complete(WidgetWrap):
    def __init__(self):
        box = "┌─┐\n│x│\n└─┘"
        super().__init__(Filler(Text(box)))


class CompleteUnplanned(WidgetWrap):
    def __init__(self):
        box = "   \n x \n   "
        super().__init__(Filler(Text(box)))


class Interrupt(WidgetWrap):
    def __init__(self):
        box = "┌─┐\n│'│\n└─┘"
        super().__init__(Filler(Text(box)))


class Void(WidgetWrap):
    def __init__(self):
        box = "┌─┐\n│/│\n└─┘"
        super().__init__(Filler(Text(box)))


class VoidUnplanned(WidgetWrap):
    def __init__(self):
        box = "   \n / \n   "
        super().__init__(Filler(Text(box)))
