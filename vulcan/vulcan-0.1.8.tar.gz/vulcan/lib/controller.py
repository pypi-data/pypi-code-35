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

from urwid import *

from model import VulcanModel
from prefs import prefs
from view import VulcanView

"""
Since we're trying to use the MVC, communication between the Model and the View
should happen through here. The bulk of the logic should also be implemented here.
"""


class GraphModel:
    def get_data(self, card):
        ret = []
        val = False
        if card:
            for i, h in enumerate(card.history):
                val += int(h.success)
                ret.append([i, val])
        return ret


class EditCard(WidgetWrap):

    def __init__(self, controller, card=None):
        self.card = card
        self.controller = controller
        self.preamble = Edit(caption="Preamble:\n", multiline=True, edit_text=(card.preamble if card else ''))
        self.question = Edit(caption="Question:\n", multiline=True, edit_text=(card.question if card else ''))
        self.answer =   Edit(caption="Answer:\n", multiline=True, edit_text=(card.answer if card else ''))
        self.tag = Edit(caption="Tag:\n", edit_text=(card.context if card else ''))
        ok = Button(label="Edit" if card else "Add")
        cancel = Button(label="Return")
        connect_signal(ok, 'click', self.ok_pressed)
        connect_signal(cancel, 'click',
            lambda button:controller.cancel_card_inserted())

        line = Divider(u'_')

        lw = SimpleFocusListWalker([
            self.preamble,
            AttrMap(line, 'line'),
            self.question,
            AttrMap(line, 'line'),
            self.answer,
            AttrMap(line, 'line'),
            self.tag,
            AttrMap(line, 'line'),
            ok,
            cancel
            ])

        lb = ListBox(lw)
        super(EditCard, self).__init__(lb)

    def reset_fields(self):
        self.question.set_edit_text('')
        self.answer.set_edit_text('')
        self.preamble.set_edit_text('')
        self.tag.set_edit_text('')

    def ok_pressed(self, button):
        if self.card:
            self.card.question = self.question.edit_text
            self.card.answer = self.answer.edit_text
            self.card.preamble = self.preamble.edit_text
            self.card.context = self.tag.edit_text
            self.controller.commit()
            self.controller.cancel_card_inserted()
        else:
            self.controller.new_card_inserted(
                question=self.question.edit_text,
                answer=self.answer.edit_text,
                preamble=self.preamble.edit_text,
                tag=self.tag.edit_text)
            self.reset_fields()


class VulcanController:
    """
    A class responsible for setting up the model and view and running
    the application.
    """
    def __init__(self, db_path):
        self.__card = None
        self.__model = VulcanModel(db_path)
        self.graph_model = GraphModel()
        self.view = VulcanView(controller=self)

    def main(self, screenshot_mode=False):
        palette = [
            ('heading', 'black', 'light gray'),
            ('line', 'black', ''),
            ('options', 'dark gray', 'black'),
            ('focus heading', 'white', 'dark red'),
            ('focus line', 'black', 'dark red'),
            ('focus options', 'black', 'light gray'),
            ('dark blue', 'dark blue', '', 'standout'),
            ('dark green', 'dark green', '', 'standout'),
            ('brown', 'brown', '', 'standout'),
            ('bg 1',         'black',      'dark blue', 'standout'),
            ('bg 1 smooth',  'dark blue',  'black'),
            ('bg 2',         'black',      'dark cyan', 'standout'),
            ('bg 2 smooth',  'dark cyan',  'black'),
            ('bg 1 smooth',  'dark blue',  'black'),
            ('bg background','black', 'black'),
        ]

        focus_map = {
            'heading': 'focus heading',
            'options': 'focus options',
            'line': 'focus line'}

        if screenshot_mode:
            palette.extend([
                ('line', 'white', 'light gray'),
                ('', 'white', 'light gray'),
                (None, 'white', 'light gray'),
            ])

        self.loop = MainLoop(widget=self.view, palette=palette, unhandled_input=self.unhandled_input)
        self.loop.run()

    def set_tag(self, tag, state):
        prefs["tag_"+tag] = state
        self.__model.tags[tag] = state
        self.__model.init_algo()

    def get_graph_data(self):
        return self.graph_model.get_data(self.__card)

    def draw_card(self):
        self.__card = self.__model.draw_card()
        if hasattr(self, 'view'):
            self.view.update_graph()
        return self.__card

    def reply(self, *args, **kwargs):
        self.__model.algo.reply(*args, **kwargs)

    def get_tags(self):
        return self.__model.tags.items()

    def commit(self):
        self.__model.algo.session.commit()

    def new_card_inserted(self, question, answer, tag='', preamble=''):
        self.__model.add_card(question=question, answer=answer, context=tag, preamble=preamble)
        self.__model.refresh_tags()
        self.view.footer.set_text("Card added successfully")
        self.view.refresh_tags()
        self.view.update_graph()

    def card_edited(self):
        self.view.columns.widget_list[0] = self.view.term
        self.__model.refresh_tags()
        self.view.refresh_tags()
        self.view.columns.widget_list.append(self.view.sidebar)
        self.view.update_graph()

    def cancel_card_inserted(self):
        # self.view.sidebar = self.view.tag_controls()
        self.view.columns.widget_list.append(self.view.sidebar)
        self.view.columns.widget_list[0] = self.view.term
        self.__model.refresh_tags()
        self.view.refresh_tags()
        self.view.terminal.draw_card()
        self.view.update_graph()

    def unhandled_input(self, key):
        """
        Handle Keyboard Input Here
        """
        if key == 'ctrl n':
            # On New Card
            self.view.columns.widget_list.pop()
            self.view.columns.widget_list[0] = EditCard(self)
        elif key == 'ctrl e':
            # On Edit Card
            self.view.columns.widget_list.pop()
            self.view.columns.widget_list[0] = EditCard(self, card=self.__card)
        elif key == 'ctrl p':
            # On Peek
            self.view.terminal.peek()
        elif key == 'f1':
            self.view.open_help_dialog()
        elif key == 'f3':
            self.view.open_grid_dialog()
        elif key == 'f5':
            self.view.open_stats_dialog()
        elif key == 'ctrl b':
            self.__model.pause_card(self.__card)
            self.view.terminal.card = None
            self.__model.refresh_tags()
            self.view.columns.widget_list[2] = self.view.sidebar
            self.view.terminal.draw_card()
        elif key == 'ctrl d':
            # On Card Deletion
            if self.view.terminal.card:
                self.__model.remove_card(self.view.terminal.card)
                self.view.terminal.card = None
                self.__model.refresh_tags()
                self.view.columns.widget_list[2] = self.view.sidebar
                self.view.terminal.draw_card()
