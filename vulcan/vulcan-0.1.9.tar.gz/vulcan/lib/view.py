# -*- coding: utf-8 -*-

# Copyright (C) 2019 github.com/shyal
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


from textwrap import dedent
from urwid import *
import vulcan.lib.utils
from vulcan.lib.store import get_session, Card
from vulcan.lib.prefs import prefs
from vulcan.lib.terminal import VulcanTerminal


class VulcanView(WidgetPlaceholder):
    """
    A class responsible for providing the application's interface and
    graph display.
    """
    def __init__(self, controller):
        self.controller = controller
        super(VulcanView, self).__init__(SolidFill(u'/'))

        self.main_window()

    def on_mode_button(self, button, state):
        """Notify the controller of a new mode setting."""
        self.controller.set_tag(button.get_label(), state)
        self.terminal.draw_card()

    def exit_program(self, w=None):
        prefs.close()
        raise ExitMainLoop()

    def refresh_tags(self):
        """
        Loop through the tags available from the model
        and either update, or add them to the list walker
        """
        for k, v in self.controller.get_tags():
            cb = list(filter(lambda x: x.get_label() == k, self.lw))
            if len(cb):
                cb = cb[0]
                cb.set_state(v)
            else:
                self.lw.append(CheckBox(label=k, state=v, on_state_change=self.on_mode_button))

        # we also need to handle removal..
        model_tags = set([k for k, v in self.controller.get_tags()])
        list_walker_tags = set([x.get_label() for x in self.lw])
        to_remove = list_walker_tags - model_tags
        for tr in to_remove:
            self.lw.remove(tr)

    def bar_graph(self):
        return BarGraph(['bg background','bg 1','bg 1'])

    def update_graph(self, force_update=False):
        l = self.controller.get_graph_data()
        if len(l) > 2:
            self.graph.set_data(l, max([x[1] for x in l]) + 1)
        else:
            self.graph.set_data([], 0)
        return True

    def tag_controls(self):
        self.lw = SimpleListWalker([])
        self.refresh_tags()
        self.graph = self.bar_graph()
        self.graph_wrap = WidgetWrap( self.graph )
        self.update_graph()
        p = Pile([
            ('fixed', 1, ListBox([Text("Tags",align="center")])),
            ('weight', 1, ListBox(self.lw)),
            ('weight', 1, self.graph_wrap),
            ('fixed', 1, ListBox([Button("Quit", self.exit_program)]))
            ])
        return p

    def ok_pressed(self, _):
        self.original_widget = self.the_first


    def main_window(self):
        lw = SimpleListWalker([])
        self.term = ListBox(lw)
        self.vline = AttrWrap(SolidFill(u'\u2502'), 'line')
        self.sidebar = self.tag_controls()

        self.columns = Columns([
            ('weight', 3, self.term),
            ('fixed', 1, self.vline), ('weight', 1, self.sidebar)],
            dividechars=1, focus_column=0)

        self.header = AttrWrap(Columns([
            ('weight', 1, Text('vulcan 1.0')),
            ('weight', 1, Text('f1:help')),
            ('weight', 1, Text('f3:grid')),
            ('weight', 1, Text('f5:stats')),
        ]), 'bg 1 smooth')
        self.footer = AttrWrap(Text(""), 'bg 1 smooth')

        # the terminal should exist in the controller, not in the view
        self.terminal = VulcanTerminal(lw=lw, controller=self.controller, view=self, multiline=True)

        frame = Frame(body=self.columns, footer=self.footer, header=self.header)

        self.original_widget = Overlay(frame, self.original_widget, align='center', width=('relative', 100),
            valign='middle', height=('relative', 100),
            min_width=24, min_height=8)

        self.the_first = self.original_widget

    def open_help_dialog(self):

        ok = Button('Close')
        connect_signal(ok, 'click', self.ok_pressed)

        nested = AttrWrap(LineBox(ListBox(
            [
                Text(dedent("""
                    Vulcan: remember anything.

                    RTVM: read the vulcan manual at https://vulcan.sh

                    Keyboard Shortcuts:

                    ?           -       open this help menu
                    ctrl n      -       open add card menu
                    ctrl e      -       edit current card
                    ctrl d      -       delete current card

                    """)),
                Text(dedent("""
                                                        _____
                                               __...---'-----`---...__
                                          _===============================
                         ______________,/'      `---..._______...---'
                        (____________LL). .    ,--'
                         /    /.---'       `. /
                        '--------_  - - - - _/
                                  `~~~~~~~~'

                    """)),
                ok
            ]
        )), 'bg 1')

        self.original_widget = Overlay(nested, self.original_widget, align='center', width=('relative', 70),
            valign='middle', height=('relative', 70),
            min_width=10, min_height=8)


    def open_stats_dialog(self):

        ok = Button('Close')
        connect_signal(ok, 'click', self.ok_pressed)
        
        session = get_session()

        query = session.query(Card)

        nested = AttrWrap(LineBox(ListBox(
            [
                Text(dedent(f"""
                    Vulcan stats.

                    {utils.stats(total=True)}
                    {utils.stats(today=True)}

                    questions asked: {sum([x.attempts for x in query])}
                    successes: {sum([x.successes for x in query])}
                    failures: {sum([x.failures for x in query])}

                    """)),
                ok
            ]
        )), 'bg 1')

        self.original_widget = Overlay(nested, self.original_widget, align='center', width=('relative', 70),
            valign='middle', height=('relative', 70),
            min_width=10, min_height=8)



    def open_grid_dialog(self):

        ok = Button('Close')
        connect_signal(ok, 'click', self.ok_pressed)
        
        session = get_session()

        query = session.query(Card)

        w = {
            'ID': 5,
            'Tag': 10,
        }

        cards = [Columns([
                ('fixed', w['ID'], Text('ID')),
                ('fixed', 3, Text(' | ')),
                ('fixed', w['Tag'], Text('Tag')),
                ('fixed', 3, Text(' | ')),
                ('weight', 1, Text('Question')),
                ('fixed', 3, Text(' | ')),
                ('weight', 1, Text('Answer')),
                ('fixed', 3, Text(' | ')),
                ('weight', 1, Text('CSuccesses')),
                ('fixed', 3, Text(' | ')),
                ('weight', 1, Text('CFailures')),
                ('fixed', 3, Text(' | ')),
            ])]

        for card in query:
            cards.append(Columns([
                ('fixed', w['ID'], Text(str(card.id))),
                ('fixed', 3, Text(' | ')),
                ('fixed', w['Tag'], Text(str(card.context[:20]))),
                ('fixed', 3, Text(' | ')),
                ('weight', 1, Text(str(card.question[:20]))),
                ('fixed', 3, Text(' | ')),
                ('weight', 1, Text(str(card.answer[:20]))),
                ('fixed', 3, Text(' | ')),
                ('weight', 1, Text(str(card.successes))),
                ('fixed', 3, Text(' | ')),
                ('weight', 1, Text(str(card.failures))),
                ('fixed', 3, Text(' | ')),
            ]))

        cards.append(ok)

        nested = AttrWrap(LineBox(ListBox(cards)), 'bg 1')

        self.original_widget = Overlay(nested, self.original_widget, align='center', width=('relative', 90),
            valign='middle', height=('relative', 90),
            min_width=10, min_height=8)



