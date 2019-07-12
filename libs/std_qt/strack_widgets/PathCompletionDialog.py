# coding=utf8
# Copyright (c) 2018 CineUse
import sys
import os

from Qt import QtCore

import std_qt
from std_py.AdvFormatter import AdvFormatter
from std_py.parse_variable_in_string import parse_variable_in_string

current_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.dirname(current_dir))
UI = os.path.join(current_dir, "path_completion_dialog.ui")
FormClass, BaseClass = std_qt.load_ui_type(UI)


class PathVariableModel(QtCore.QAbstractTableModel):

    def __init__(self, parent=None):
        super(PathVariableModel, self).__init__(parent)

        self.__variable_dict = {}

    @property
    def variable_list(self):
        return self.__variable_dict.keys()

    @property
    def variable_dict(self):
        return self.__variable_dict

    @variable_dict.setter
    def variable_dict(self, value):
        if isinstance(value, dict):
            self.__variable_dict = value
        else:
            raise TypeError('expected a list object, but got a %s object.' % type(value).__name__)

    def rowCount(self, index=QtCore.QModelIndex()):
        return len(self.variable_list)

    def columnCount(self, index=QtCore.QModelIndex()):
        return 2

    def flags(self, index):
        col = index.column()
        if col == 0:
            return QtCore.Qt.ItemIsEnabled
        else:
            return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid() and role in [QtCore.Qt.DisplayRole, QtCore.Qt.EditRole]:
            row = index.row()
            col = index.column()
            if col == 0:
                return self.variable_list[row]
            else:
                return self.variable_dict.get(self.variable_list[row])

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.isValid() and role == QtCore.Qt.EditRole:
            row = index.row()
            col = index.column()
            if col == 1:
                self.variable_dict.update({self.variable_list[row]: value})
                self.dataChanged.emit(index, index)
                return True
        return False

    def update_data(self, data):
        self.beginResetModel()
        self.variable_dict = data
        self.endResetModel()


class PathCompletionDialog(FormClass, BaseClass):

    def __init__(self, source_path='', dest_path='', parent=None):
        super(PathCompletionDialog, self).__init__(parent)
        self.__dest_path = dest_path
        self.__source_path = source_path
        self.setupUi(self)

        self.init_ui()

        self.bind_func()

    @property
    def dest_path(self):
        return self.__dest_path

    @dest_path.setter
    def dest_path(self, value):
        if isinstance(value, basestring):
            self.__dest_path = value
        else:
            raise TypeError('expected a string object, but got a %s object.' % type(value).__name__)

    def init_ui(self):
        self.source_value_label.setText(self.__source_path)
        self.path_value_label.setText(self.dest_path)
        variable_list = parse_variable_in_string(self.dest_path)
        variable_dict = {}
        for variable in variable_list:
            variable_dict.setdefault(variable, '')
        self.item_model = PathVariableModel(self.table_view)
        self.table_view.setModel(self.item_model)
        self.item_model.update_data(variable_dict)

    def bind_func(self):
        self.item_model.dataChanged.connect(self.generate_result)

    def generate_result(self, *args):
        variable_dict = self.item_model.variable_dict
        fmt = AdvFormatter()
        result = fmt.format(self.dest_path, **variable_dict)
        self.path_value_label.setText(result)

    @classmethod
    def complete_path(cls, source_path, dest_path):
        dlg = cls(source_path, dest_path)
        flag = dlg.exec_()
        return flag, dlg.item_model.variable_dict


if __name__ == "__main__":
    PathCompletionDialog()
