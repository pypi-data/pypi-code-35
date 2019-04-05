# This file is part of Sympathy for Data.
# Copyright (c) 2013 System Engineering Software Society
#
# Sympathy for Data is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Sympathy for Data is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Sympathy for Data.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
import Qt.QtCore as QtCore
import Qt.QtGui as QtGui
import Qt.QtWidgets as QtWidgets

from sympathy.platform import qt_support as platform_qt_support
from sympathy.platform import widget_library as sywidgets
from sympathy.utils import search


def font_color_highlighter(color='#990000', **kw):
    return 'color="{}"'.format(color)


def font_background_highlighter(color='#EECC22', **kw):
    return 'style="background-color: {}"'.format(color)


def font_weight_highlighter(**kw):
    return 'style="font-weight: bold"'


def style_font_weight_bold(text):
    return f'<font style="font-weight: bold">{text}</font>'


highlighters = {
    'color': font_color_highlighter,
    'background-color': font_background_highlighter,
    'font-weight': font_weight_highlighter
}


IdentityRole = QtCore.Qt.UserRole
HighlightRole = QtCore.Qt.UserRole + 1
BoldRole = QtCore.Qt.UserRole + 2
PositionRole = QtCore.Qt.UserRole + 3


class Highlighter(QtWidgets.QStyledItemDelegate):
    def __init__(self, highlight_on, highlight_role, parent, *args):
        super().__init__(parent, *args)
        self._highlight_role = highlight_role
        self._highlight_on = highlight_on

    def set_highlight_on(self, state):
        self._highlight_on = state

    def paint(self, painter, option, index):
        options = QtWidgets.QStyleOptionViewItem(option)
        self.initStyleOption(options, index)

        if options.widget is None:
            style = QtWidgets.QApplication.style()
        else:
            style = options.widget.style()

        doc = QtGui.QTextDocument()
        text = index.data(HighlightRole)
        doc.setHtml(text)

        options.text = ""
        style.drawControl(QtWidgets.QStyle.CE_ItemViewItem, options, painter)

        ctx = QtGui.QAbstractTextDocumentLayout.PaintContext()

        # Highlighting text if item is selected
        if (options.state & QtWidgets.QStyle.State_Selected):
            ctx.palette.setColor(
                QtGui.QPalette.Text,
                options.palette.color(
                    QtGui.QPalette.Active, self._highlight_role))

        text_rect = style.subElementRect(
            QtWidgets.QStyle.SE_ItemViewItemText, options, None)
        painter.save()
        painter.translate(text_rect.topLeft())
        painter.setClipRect(text_rect.translated(-text_rect.topLeft()))
        doc.documentLayout().draw(painter, ctx)

        painter.restore()

    def sizeHint(self, option, index):
        size_hint = super().sizeHint(option, index)
        options = QtWidgets.QStyleOptionViewItem(option)
        self.initStyleOption(options, index)

        doc = QtGui.QTextDocument()
        doc.setHtml(index.data(HighlightRole))
        doc.setTextWidth(options.rect.width())
        return QtCore.QSize(
            doc.idealWidth(), max(doc.size().height(), size_hint.height()))


class LeafItem(object):
    """Interface that items of the TreeModel must fulfill."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._name = ''
        self._highlighted_text = ''
        self._parent = None

    def name(self):
        return self._name

    def parent(self):
        return self._parent

    def is_leaf(self):
        return True

    def child_count(self):
        return 0

    def icon(self):
        return None

    def identifier(self):
        """
        Unique identifier, used for drag operations
        """
        return None

    def tool_tip(self):
        return ''

    def row(self):
        """Find out which row the current item has (below its parent)"""
        if self._parent:
            return self._parent.index(self)
        else:
            return 0

    def highlighted(self):
        """Highlighted text"""
        return self._highlighted_text

    def set_highlighted_text(self, text):
        """Set Highlighted text"""
        self._highlighted_text = text

    def node(self):
        """Not valid for parents"""
        return None


class TreeItem(LeafItem):
    def __init__(self, *args, **kwargs):
        self._children = []
        super().__init__(*args, **kwargs)

    def is_leaf(self):
        return False

    def add_child(self, child):
        """Add a child"""
        self._children.append(child)

    def remove_child(self, child):
        self._children.remove(child)

    def insert_child(self, i, child):
        self._children.insert(i, child)

    def index(self, child):
        """Returns the index of child"""
        return self._children.index(child)

    def child(self, row):
        """Returns the child at row"""
        return self._children[row]

    def child_count(self):
        return len(self._children)


class TreeModel(QtCore.QAbstractItemModel):

    """
    Responsible for building and updating the (viewed) tree.
    """

    def __init__(self, root_item, parent=None):
        super().__init__(parent)
        self._root = root_item
        self._old_root = None
        self._index_to_item = {}
        self._item_enumerator = platform_qt_support.object_enumerator()
        self._build_model()

    def _build_model(self):
        raise NotImplementedError

    @QtCore.Slot()
    def update_model(self):
        self.beginResetModel()
        self._build_model()
        self.endResetModel()

    def createIndex(self, row, column, item):
        # Internal ID is set based on the attached pointer.
        # We manage this ourselves since putting an object as internalPointer
        # seems to be unstable in Python.
        # http://www.riverbankcomputing.com/pipermail/pyqt/2009-April/022709.html
        index = super().createIndex(
            row, column, self._item_enumerator(item))
        self._index_to_item[index.internalId()] = item
        return index

    #
    # QAbstractItemModel interface
    #

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 1

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            item = self._index_to_item.get(parent.internalId())
            if item is None:
                return 0
            return item.child_count()
        else:
            return self._root.child_count()

    def index(self, row, column, parent=QtCore.QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if parent.isValid():
            parent_item = self._index_to_item.get(parent.internalId())
        else:
            parent_item = self._root

        child_item = None
        if parent_item is not None:
            child_item = parent_item.child(row)

        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        empty_index = QtCore.QModelIndex()

        if not index.isValid():
            return empty_index

        item = self._index_to_item.get(index.internalId())
        if item:
            parent = item.parent()
            if parent and parent.parent():
                return self.createIndex(parent.row(), 0, parent)

        return empty_index

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        item = self._index_to_item.get(index.internalId())

        if item is None:
            pass
        elif role == QtCore.Qt.DisplayRole:
            name = item.name()
            return name[:1].upper() + name[1:]
        elif role == QtCore.Qt.DecorationRole:
            return item.icon()
        elif role == QtCore.Qt.ToolTipRole:
            return item.tool_tip()
        elif role == IdentityRole:
            return item.identifier()
        elif role == HighlightRole:
            return item.highlighted()

    def setData(self, index, value, role):
        if not index.isValid():
            return None
        if role == HighlightRole:
            item = self._index_to_item.get(index.internalId())
            item.set_highlighted_text(value)
        else:
            super().setData(index, value, role)

    def itemData(self, index):
        item = self._index_to_item.get(index.internalId())
        data = None
        if item is not None:
            data = item.node()
        return data

    def flags(self, index):
        if not index.isValid():
            return 0

        item = self._index_to_item.get(index.internalId())

        if item is not None and item.is_leaf():
            return (QtCore.Qt.ItemIsEnabled |
                    QtCore.Qt.ItemIsDragEnabled |
                    QtCore.Qt.ItemIsSelectable)
        else:
            return (QtCore.Qt.ItemIsEnabled |
                    QtCore.Qt.ItemIsSelectable)

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.TextAlignmentRole:
            if orientation == QtCore.Qt.Horizontal:
                return QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
            else:
                return QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter
        elif role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return 'Node name'
            else:
                return section + 1
        else:
            return None


class TreeView(QtWidgets.QTreeView):
    """
    Tree view. It is separated from the regular tree view in order to support
    selection_changed signalling.
    """

    selection_changed = QtCore.Signal(dict)
    switch_to_filter = QtCore.Signal()
    item_accepted = QtCore.Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._font = QtWidgets.QApplication.font()

        # Workaround, primarily for Windows. If highlightedText is opaque we
        # assume that it is not used. This also relates to why transparent
        # backgrounds are used in stylesheets.
        highlight_opaque = self.palette().highlightedText().isOpaque()
        self._highlight_role = QtGui.QPalette.HighlightedText
        if highlight_opaque:
            self._highlight_role = QtGui.QPalette.Text
        highlighter = Highlighter(
            highlight_on=False, highlight_role=self._highlight_role,
            parent=self)

        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setIndentation(15)
        self.setDropIndicatorShown(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)
        self.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.setUniformRowHeights(True)
        self.setHeaderHidden(True)
        self.setFont(self._font)
        self.setItemDelegate(highlighter)
        self.doubleClicked.connect(self._accept_index)

    def set_highlight_mode(self, highlight_on=False):
        item_delegate = self.itemDelegate()
        item_delegate.set_highlight_on(highlight_on)
        if highlight_on:
            # this is prevents showing the branch icons in the FlatTag mode
            if self._highlight_role == QtGui.QPalette.HighlightedText:
                self.setStyleSheet(
                    'QTreeView::branch { border-image: url(none.png); }')
            else:
                self.setStyleSheet(
                    'QTreeView {'
                    '  border-image: url(none.png);'
                    '  selection-background-color: transparent; }')
        else:
            if self._highlight_role != QtGui.QPalette.HighlightedText:
                self.setStyleSheet(
                    'QTreeView { selection-background-color: transparent; }')

    def selectionChanged(self, selected, deselected):
        if len(selected.indexes()) > 0:
            index = self.model().mapToSource(selected.indexes()[0])
            self.selection_changed.emit(
                self.model().sourceModel().itemData(index))
        super().selectionChanged(selected, deselected)

    def keyPressEvent(self, event):
        index = self.currentIndex()
        parent = index.parent()
        if (event.key() == QtCore.Qt.Key_Up and parent and
                parent.row() == 0 and index.row() == 0):
            self.switch_to_filter.emit()
        elif event.key() == QtCore.Qt.Key_Return:
            proxy_index = self.currentIndex()
            self._accept_index(proxy_index)
            event.accept()
        else:
            super().keyPressEvent(event)

    def focusOutEvent(self, event):
        self.setCurrentIndex(QtCore.QModelIndex())
        super().focusOutEvent(event)

    def _accept_index(self, index):
        index = self.model().mapToSource(index)
        item = self.model().sourceModel().itemData(index)
        self._accept_item(item)

    def _accept_item(self, item):
        self.item_accepted.emit(item)


class AdvancedFilter(QtWidgets.QWidget):
    switch_to_list = QtCore.Signal()
    filter_changed = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self._init_gui()

    def _init_gui(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(QtCore.QMargins())

        self._filter = FilterLineEdit(parent=self)
        layout.addWidget(self._filter)
        self._filter.switch_to_list.connect(self.switch_to_list)
        self._filter.textChanged[str].connect(self.filter_changed)
        self.setLayout(layout)

    def set_focus(self):
        # TODO: if enhanced mode is open, set focus to lowest LineEdit widget
        self._filter.setFocus()


class FilterLineEdit(sywidgets.ClearButtonLineEdit):
    switch_to_list = QtCore.Signal()

    def __init__(self, placeholder="Filter", clear_button=True, parent=None):
        super().__init__(placeholder, clear_button, parent)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Down:
            self.switch_to_list.emit()
            # event.accept()
        else:
            super().keyPressEvent(event)


class FilterTreeView(QtWidgets.QWidget):
    """Combination widget - tree view and filter edit."""

    item_accepted = QtCore.Signal(object)

    def __init__(self, proxy_model, view, parent=None):
        super().__init__(parent)
        self._proxy_model = proxy_model
        self._model = None

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setContentsMargins(QtCore.QMargins())
        self._layout.setSpacing(0)

        self._filter = AdvancedFilter(parent=self)
        self._layout.addWidget(self._filter)
        self._view = view
        self._view.setModel(self._proxy_model)
        self._layout.addWidget(self._view, stretch=10)

        self.update_filter('')

        self._filter.filter_changed[str].connect(
            self.update_filter)
        self._filter.switch_to_list.connect(self._handle_switch_to_list_view)
        self._view.switch_to_filter.connect(self._handle_switch_to_filter)
        self._view.item_accepted.connect(self.item_accepted)
        self.setLayout(self._layout)

    def set_model(self, model):
        # Store model as a private member to avoid shiboken
        # deallocation problem.
        self._model = model
        self._reset_model()
        self._setup_view()
        self._model.modelReset.connect(self._reset_model)

    def _setup_view(self):
        self._view.setIndentation(15)
        self._view.setItemsExpandable(True)
        self._view.set_highlight_mode(False)

    def _default_expand(self):
        self._view.collapseAll()

    @QtCore.Slot()
    def update_model(self):
        self._model.update_model()

    @QtCore.Slot(tuple)
    def set_highlighter(self, highlighter_param):
        matcher_type, highlighter_type, highlighter_color = highlighter_param
        highlighter_func = highlighters.get(highlighter_type,
                                            font_color_highlighter)
        highlighter_attr = highlighter_func(color=highlighter_color)
        self._proxy_model.highlighter_attr = highlighter_attr
        self._proxy_model.matcher_type = matcher_type

    @QtCore.Slot()
    def _reset_model(self):
        """Reset (reload) model"""
        sort_role = self._proxy_model.sortRole()
        self._proxy_model.setSourceModel(self._model)
        self._proxy_model.setSortRole(sort_role)
        self.update_filter()

    @QtCore.Slot(str)
    def update_filter(self, new_filter=None):
        used_filter = self._proxy_model.update_filter(new_filter)
        self._handle_expanding(used_filter != '')

    def focus_filter(self):
        self._filter.set_focus()

    @QtCore.Slot()
    def clear_filter(self):
        self._filter.setText('')
        self.update_filter('')
        self._view.collapseAll()

    def _handle_expanding(self, state):
        if state:
            self._view.expandAll()
        else:
            self._default_expand()

    def _handle_switch_to_list_view(self):
        self._view.setFocus()
        try:
            proxy_index = self._proxy_model.index(0, 0)
            self._view.setCurrentIndex(proxy_index)
        except Exception:
            pass

    def _handle_switch_to_filter(self):
        self._filter.set_focus()
        self._view.setCurrentIndex(QtCore.QModelIndex())

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            view = self._view
            proxy_index = view.currentIndex()
            index = self._proxy_model.mapToSource(proxy_index)
            item = self._proxy_model.sourceModel().itemData(index)
            self.item_accepted.emit(item)
            event.accept()
        super().keyPressEvent(event)


class TreeFilterProxyModelBase(QtCore.QSortFilterProxyModel):
    """
    Proxy model that supplies sorting and filtering for the tree model.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._filter = ''
        self._output_type = None
        self._cache = {}
        self._matcher_type = 'character'
        self._highlighter_attr = 'style="background-color: #EECC22"'
        self._filter_regex = None
        self._highlight_regex = []
        self.highlighted = set()

    @property
    def matcher_type(self):
        return self._matcher_type

    @matcher_type.setter
    def matcher_type(self, matcher_type):
        self._matcher_type = matcher_type
        self.update_filter(self._filter)

    @property
    def highlighter_attr(self):
        return self._highlighter_attr

    @highlighter_attr.setter
    def highlighter_attr(self, attr):
        self._highlighter_attr = attr
        self.update_filter(self._filter)

    def filterAcceptsRow(self, source_row, source_parent):
        index = self.sourceModel().index(
            source_row, self.sourceModel().columnCount() - 1, source_parent)
        return self._show_row(index)

    def _show_row(self, index):
        ret_val = False
        source = self.sourceModel()
        number_of_rows = source.rowCount(index)

        if number_of_rows > 0:
            for i in range(number_of_rows):
                child_index = source.index(i, 0, index)
                if not child_index.isValid():
                    break
                else:
                    ret_val = self._show_row(child_index)
                if ret_val:
                    break
        else:
            parent_names = []
            parents = []

            parent = source.index(index.row(), 0, index.parent())
            parent_name = source.data(parent)

            item = source._index_to_item.get(parent.internalId())

            if not item or not self._show_item(item):
                return False

            while parent_name:
                parent_names.append(parent_name)
                parents.append(parent)
                parent = source.parent(parent)
                parent_name = source.data(parent)

            # Highlight!
            for parent, parent_name in zip(parents, parent_names):
                if self._matcher_type == 'word':
                    full_label = self.highlight_word(parent_name)
                elif self._matcher_type == 'character':
                    full_label = self.highlight_character(parent_name)
                else:
                    full_label = parent_name

                if source.data(parent, BoldRole):
                    full_label = style_font_weight_bold(full_label)

                source.setData(
                    parent, full_label, HighlightRole)

            ret_val = search.matches(
                self._filter_regex, ' '.join(list(reversed(parent_names))))

        return ret_val

    def _show_item(self, item):
        return True

    def highlight_character(self, parent_type):
        seq_to_highlight = set()
        for rx in self._highlight_regex:
            org_filter = rx.pattern.replace('\\S*?', '')
            text = parent_type.replace('/', ' ')
            for c in '(*^-.?${},+[])':
                org_filter = org_filter.replace('\\{}'.format(c), c)
            for m in rx.finditer(text):
                i = 0
                sub_string = m.group().lower()
                for c in org_filter:
                    i += sub_string[i:].index(c.lower()) + 1
                    seq_to_highlight.add(i + m.start())

        seq_to_highlight = np.atleast_1d(list(seq_to_highlight))
        seq_to_highlight.sort()
        if len(seq_to_highlight) == 0:
            sub_matches = []
        elif len(seq_to_highlight) == 1:
            sub_matches = [seq_to_highlight]
        else:
            pos_diff = np.diff(seq_to_highlight)
            is_not_consecutive = np.hstack(
                ([False], pos_diff > 1))
            split_indices = np.where(is_not_consecutive)[0]
            sub_matches = np.split(seq_to_highlight, split_indices)

        highlighted_text = list(parent_type)
        addon = 0
        for sub_match in sub_matches:
            highlighted_text.insert(
                min(sub_match) + addon - 1,
                '<font {}>'.format(self.highlighter_attr))
            addon += 1
            highlighted_text.insert(
                max(sub_match) + addon, '</font>')
            addon += 1
        full_label = ''.join(highlighted_text)
        return full_label

    def highlight_word(self, parent_type):
        full_label = []
        for word in parent_type.split(' '):
            matches = [f.search(word) for f in
                       self._highlight_regex]
            matches = [m for m in matches if m is not None]
            matches.sort(key=lambda x: x.start())
            highlighted_text = list(word)
            addon = 0
            for match in matches:
                if match.start() < match.end():
                    highlighted_text.insert(
                        match.start() + addon,
                        '<font {}>'.format(self.highlighter_attr))
                    addon += 1
                    highlighted_text.insert(match.end() + addon,
                                            '</font>')
                    addon += 1
            full_label.append(''.join(highlighted_text))
        full_label = ' '.join(full_label)
        return full_label

    def update_filter(self, new_filter):
        if new_filter is not None:
            self._highlight_regex = search.highlight_patterns(new_filter)
            self._filter = new_filter
            self._filter_regex = search.fuzzy_pattern(new_filter)

        sort_role = self.sortRole()
        self.invalidateFilter()
        self.setSortRole(sort_role)
        self.sort(0, QtCore.Qt.AscendingOrder)
        return self._filter
