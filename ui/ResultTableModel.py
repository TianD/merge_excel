# coding:utf-8

import pandas as pd
from Qt import QtCore


class ResultTableModel(QtCore.QAbstractTableModel):

    def __init__(self, source_data, parent=None):
        super(ResultTableModel, self).__init__(parent)
        self.__source_data = source_data

    @property
    def source_data(self):
        return self.__source_data.values.tolist()

    @property
    def headers(self):
        return self.__source_data.columns.values.tolist()

    def rowCount(self, parent=QtCore.QModelIndex()):
        if self.__source_data.empty:
            return 0
        return len(self.source_data)

    def columnCount(self, parent=QtCore.QModelIndex()):
        if self.__source_data.empty:
            return 0
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
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled