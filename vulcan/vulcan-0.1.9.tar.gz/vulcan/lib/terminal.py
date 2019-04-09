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

from functools import partial
from urwid import Edit, Text

import vulcan.lib.context as ctx


def wrong_cb(given_answer, right_answer, lw):
    lw.append(Text("wrong.. you wrote:"))
    lw.append(Text(given_answer))
    lw.append(Text("please remember:"))
    lw.append(Text(right_answer))


class VulcanTerminal(Edit):

    """
    This class may be totally overcomplicated.
    """

    def __init__(self, lw, controller, view, *args, **kwargs):
        self.lw = lw
        self.controller = controller
        self.view = view
        self.card = None
        super(VulcanTerminal, self).__init__(*args, **kwargs)
        self.draw_card()

    def draw_card(self):
        new_card = self.controller.draw_card()
        if new_card:
            if self.card != new_card:
                self.card = new_card
                try:
                    self.lw.remove(self)
                except:
                    pass
                self.card_context = ctx.prompt(self.card)
                if self.card_context.command:
                    self.lw.append(Text(ctx.bash_prompt() + self.card_context.command))
                self.lw.append(Text(self.card_context.render()))
                self.lw.append(self)
                self.lw.set_focus(len(self.lw) - 1)
                self.set_caption(self.card_context.prompt)
                self.view.update_graph()
        else:
            self.view.footer.set_text("No Cards - press ctrl-n to insert a new one")

    def peek(self):
        try:
            self.lw.remove(self)
        except:
            pass
        self.lw.append(Text(self.card.answer))
        self.lw.set_focus(len(self.lw) - 1)
        self.set_caption(self.card_context.prompt)

    def keypress(self, size, key):
        fin_multi = self.card.multi and len(self.edit_text) and key == 'enter' and self.edit_text[-1] == '\n'
        fin_norm =  ((not self.card.multi) and key == 'enter')
        if (not (fin_norm or fin_multi)):
            return super(VulcanTerminal, self).keypress(size, key)
        self.lw.append(Text(self.card_context.prompt + [self.edit_text]))
        self.controller.reply(self.card.id, self.card.compare_answer(self.edit_text), self.edit_text, partial(wrong_cb, lw=self.lw))
        self.draw_card()
        self.set_edit_text('')
        self.lw.set_focus(len(self.lw)-1)