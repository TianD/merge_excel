# coding:utf-8

import pandas as pd

from Qt import QtCore
from Qt import QtWidgets
from std_qt.strack_widgets.MultiComboBox import MultiComboBox


class MatchedColumnDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, parent=None):
        super(MatchedColumnDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        model = index.model()
        row = index.row()
        excel_path = model.source_data[row][0]
        current_value = model.source_data[row][1]
        excel_data = pd.read_excel(excel_path, sheet_name=0)
        column_list = excel_data.columns.values.tolist()
        current_index = next((i for i, column in enumerate(column_list) if column == current_value), 0)
        combobox = QtWidgets.QComboBox(parent)
        combobox.addItems(column_list)
        combobox.setCurrentIndex(current_index)
        return combobox

    def setModelData(self, editor, model, index):
        current_text = editor.currentText()
        model.setData(index, current_text)
        model.dataChanged.emit(index, index)


class AdditionColumnDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, parent=None):
        super(AdditionColumnDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        model = index.model()
        row = index.row()
        excel_path = model.source_data[row][0]
        current_value = model.source_data[row][-1]
        excel_data = pd.read_excel(excel_path, sheet_name=0)
        column_list = excel_data.columns.values.tolist()
        current_index_list = [i for i, column in enumerate(column_list) if column in current_value.split(';')]
        combobox = MultiComboBox(parent)
        combobox.addItems(column_list)
        combobox.set_checked_index(current_index_list)
        return combobox

    def setModelData(self, editor, model, index):
        current_text = editor.currentText()
        model.setData(index, current_text)
        model.dataChanged.emit(index, index)


class AdditionTableModel(QtCore.QAbstractTableModel):

    def __init__(self, source_data=None, parent=None):
        super(AdditionTableModel, self).__init__(parent)
        self.__source_data = source_data or list()
        self.__headers = [u'Excel路径', u'名称匹配列', u'起始时码匹配列', u'结束时码匹配列', u'添加列']

    @property
    def source_data(self):
        return self.__source_data

    @property
    def headers(self):
        return self.__headers

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.source_data)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.headers)

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.headers[section]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return
        row = index.row()
        column = index.column()

        if role == QtCore.Qt.DisplayRole:
            return self.source_data[row][column]

    def flags(self, index):
        if index.isValid():
            return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if not index.isValid():
            return False
        row = index.row()
        column = index.column()
        if role == QtCore.Qt.EditRole:
            self.__source_data[row][column] = value
        return True

    def appendRow(self, value):
        new_row = self.rowCount()
        parent = self.index(new_row-1, 0).parent()
        self.source_data.append(value)
        self.beginInsertRows(parent, new_row, new_row)
        super(AdditionTableModel, self).insertRow(new_row)
        self.endInsertRows()

    def removeRow(self, row, parent=QtCore.QModelIndex()):
        self.source_data.pop(row)
        self.beginRemoveRows(parent, row, row)
        super(AdditionTableModel, self).removeRow(row)
        self.endRemoveRows()
