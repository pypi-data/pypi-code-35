import xml.etree.ElementTree as ET
import functools

import tkinter as tk


class InfoText:
    def __init__(self, master):
        self.text = tk.Text(master, state=tk.DISABLED)

    def _parse(self, s):
        tokens = []
        nodes = []
        attrs_by_tag = {}

        def _push(node):
            if node.tag not in attrs_by_tag and len(node.attrib) > 0:
                attrs_by_tag[node.tag] = node.attrib

            _ = {'tag': node.tag, 'order': len(nodes), 'begin': None, 'end': None}
            nodes.append((node, _))
            tokens.append(_)
            if node.text:
                tokens.append(node.text)

        def _pop():
            node, _ = nodes.pop()
            tokens.append(_)
            if node.tail:
                tokens.append(node.tail)

        def _traverse(node):
            _push(node)

            for _ in node:
                _traverse(_)

            _pop()

        _traverse(ET.fromstring('<R-O-O-T>%s</R-O-O-T>' % s))
        return tokens, attrs_by_tag

    def clear(self):
        self.text.tag_delete(*self.text.tag_names())
        self.text.delete('1.0', tk.END)

    def show(self, s, *, funcs_by_name=None, fonts_by_name=None):
        self.text['state'] = tk.NORMAL

        tokens, attrs_by_tag = self._parse(s)
        tokens_tag = []

        self.clear()
        for i, token in enumerate(tokens):
            if isinstance(token, str):
                self.text.insert(tk.INSERT, token)
                continue

            index = self.text.index(tk.INSERT)
            if token['begin'] is None:
                token['begin'] = index
            else:
                assert token['end'] is None
                token['end'] = index

                tokens_tag.append(token)

        """https://www.tcl.tk/man/tcl8.7/TkCmd/text.htm:

        When a tag is defined (by associating it with characters or
        setting its display options or binding commands to it), it is
        given a priority higher than any existing tag.
        """

        # add tags in RIGHT order
        for i, token in enumerate(sorted(tokens_tag, key=lambda _: _['order'])):
            attrs = attrs_by_tag.get(token['tag'])
            if attrs is None:
                continue

            token['tag'] = 'TAG%04d-%s' % (i, token['tag'])  # every tag added is unique
            self.text.tag_add(token['tag'], token['begin'], token['end'])

            d = {}
            for k, v in attrs.items():
                if k == 'BINDINGS':
                    for binding in filter(None, map(str.strip, v.split(','))):
                        event_pat, func_name = map(str.strip, binding.split('=>'))
                        if funcs_by_name is not None:
                            func = funcs_by_name[func_name]
                            func = functools.partial(func, token=token)
                            self.text.tag_bind(token['tag'], '<%s>' % event_pat, func, add=True)
                    continue

                if k == 'font':
                    _ = v.split(',')
                    if len(_) > 1:
                        v = tuple(_)
                    elif fonts_by_name is not None:
                        v = fonts_by_name.get(v) or v
                d[k] = v

            if len(d) > 0:
                self.text.tag_configure(token['tag'], **d)

        self.text['state'] = tk.DISABLED
