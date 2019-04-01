from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import biseau as bs
import random


class OptionsModel(QStandardItemModel):
    def __init__(self):
        super().__init__()

    def set_script(self, script: bs.Script):
        """ 
        Create model option according script
        """
        self.script = script
        self.clear()
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["key", "value"])

        for option in self.script.options:
            default_value = option[2]
            key_item = QStandardItem(option[0])  # option name
            val_item = QStandardItem(str(default_value))  # default value ?
            Type = option[1]  # Get option type
            val_item.setData(
                Type(default_value), Qt.EditRole
            )  # cast according option type

            key_item.setEditable(False)
            self.appendRow([key_item, val_item])

    def get_option_values(self):
        """ 
        return options value according model 
        """
        option_values = {}
        for row in range(self.rowCount()):
            key = self.item(row, column=0).text()
            val = self.item(row, column=1).data(Qt.EditRole)
            option_values[key] = val

        return option_values


class OptionsWidget(QTableView):
    def __init__(self):
        super().__init__()
        self.model = OptionsModel()
        self.setModel(self.model)
        self.verticalHeader().hide()
        self.horizontalHeader().setStretchLastSection(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setAlternatingRowColors(True)

    def set_script(self, script: bs.Script):
        """
        @see OptionModel.setScript())
        """
        self.model.set_script(script)

    def get_option_values(self):
        """
        @see OptionModel.get_option_values())
        """
        return self.model.get_option_values()


# class ColorListEditor(QComboBox):
#     def __init__(self, widget=None):
#         super().__init__(widget)
#         self.populateList()

#     def getColor(self):
#         color = self.itemData(self.currentIndex(), Qt.DecorationRole)
#         return color

#     def setColor(self, color):
#         self.setCurrentIndex(self.findText(color))

#     def populateList(self):
#         for i, colorName in enumerate(QColor.colorNames()):
#             color = QColor(colorName)
#             self.insertItem(i, colorName)
#             self.setItemData(i, color, Qt.DecorationRole)

#     data = Property(QColor, getColor, setColor, user=True)


# class StackDelegate(QStyledItemDelegate):
#     def __init__(self):
#         super().__init__()

#         self.custom_editors = {
#         QColor: ColorListEditor
#         }


#     def createEditor(self,parent: QWidget, option, index):

#         data_type = type(index.data())

#         if data_type in self.custom_editors.keys():
#             Editor = self.custom_editors[data_type]
#             return Editor(parent)

#         else:
#             return super().createEditor(parent,option,index)

#     def setModelData(self, editor, model, index):

#         data_type = type(index.data())

#         if data_type in self.custom_editors.keys():
#             return model.setData(index, editor.data)

#         else:
#             return super().setModelData(editor, model, index)


#     def paint(self,painter,option,index):

#         if index.parent() == QModelIndex() and index.column() == 1:
#             progressBarOption = QStyleOptionProgressBar()
#             progressBarOption.rect = option.rect

#             progressBarOption.minimum = 0;
#             progressBarOption.maximum = 100
#             progressBarOption.textAlignment = Qt.AlignCenter
#             progressBarOption.progress = int(index.data())
#             progressBarOption.text = f"{index.data()} % "
#             progressBarOption.textVisible = True;
#             QApplication.style().drawControl(QStyle.CE_ProgressBar,progressBarOption, painter)

#         else:
#             super().paint(painter,option,index)


#     # factory = QItemEditorFactory()
#     # factory.registerEditor(1, ColorListItemEditorCreator())

#     # QItemEditorFactory.setDefaultFactory(factory)

#     self.view.setItemDelegate(self.stack_delegate)

#     v_layout = QVBoxLayout()
#     v_layout.addWidget(self.bar)
#     v_layout.addWidget(self.view)
#     v_layout.setContentsMargins(0,0,0,0)
#     v_layout.setSpacing(0)
#     v_layout.addWidget(self.w)
#     self.setLayout(v_layout)

#     # Setup toobar
#     move_up_action   = self.bar.addAction("up")
#     move_down_action = self.bar.addAction("down")


#     self.view.setModel(self.stack_model)
#     self.stack_model.add_module()
#     self.stack_model.add_module()
#     self.stack_model.add_module()
#     self.stack_model.add_module()
#     self.stack_model.add_module()

#     self.view.setSelectionMode(QAbstractItemView.SingleSelection)
#     self.view.setDragEnabled(True)
#     self.view.viewport().setAcceptDrops(True)
#     self.view.setDropIndicatorShown(True)
#     self.view.setDragDropMode(QAbstractItemView.InternalMove)

#     self.view.header().setSectionResizeMode(0,QHeaderView.Stretch)


# def contextMenuEvent(self,event):
#     """override """
#     index = self.view.indexAt(self.view.viewport().mapFromGlobal(event.globalPos()))
#     if index:
#         if index.parent() == QModelIndex():
#             menu = QMenu()
#             menu.addAction(index.data())
#             menu.exec_(event.globalPos())


# @property
# def scripts(self) -> [biseau.Script]:
#     "Iterable over Scripts described by the widget, ordered from first to last"
#     raise NotImplementedError()
