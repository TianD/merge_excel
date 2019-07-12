# coding=utf8
# Copyright (c) 2018 CineUse

import sys
from Qt import QtCore, QtGui, QtWidgets


class FlatProxyModel(QtCore.QAbstractProxyModel):
    """
    convert a tree model to a list model.
    """
    def __init__(self, parent=None):
        super(FlatProxyModel, self).__init__(parent)

    @QtCore.Slot(QtCore.QModelIndex, QtCore.QModelIndex)
    def sourceDataChanged(self, topLeft, bottomRight):
        self.dataChanged.emit(self.mapFromSource(topLeft), \
                              self.mapFromSource(bottomRight))

    def build_map(self, model, parent=QtCore.QModelIndex(), row=0):
        if row == 0:
            self.m_rowMap = {}
            self.m_indexMap = {}
        rows = model.rowCount(parent)
        for r in range(rows):
            index = model.index(r, 0, parent)
            self.m_rowMap[index] = row
            self.m_indexMap[row] = index
            row += 1
            if model.hasChildren(index):
                row = self.build_map(model, index, row)
        return row

    def setSourceModel(self, model):
        super(FlatProxyModel, self).setSourceModel(model)
        self.build_map(model)
        model.dataChanged.connect(self.sourceDataChanged)

    def mapFromSource(self, index):
        if index not in self.m_rowMap:
            return QtCore.QModelIndex()
        return self.createIndex(self.m_rowMap[index], index.column())

    def mapToSource(self, index):
        if not index.isValid() or index.row() not in self.m_indexMap:
            return QtCore.QModelIndex()
        return self.m_indexMap[index.row()]

    def columnCount(self, parent):
        return QtCore.QAbstractProxyModel.sourceModel(self) \
            .columnCount(self.mapToSource(parent))

    def rowCount(self, parent):
        return len(self.m_rowMap) if not parent.isValid() else 0

    def index(self, row, column, parent):
        if parent.isValid():
            return QtCore.QModelIndex()
        return self.createIndex(row, column)

    def parent(self, index):
        return QtCore.QModelIndex()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    model = QtGui.QStandardItemModel()
    data = {'Group1': ['a', 'b'], 'Group2': ['c', 'd'], 'Group3': ['e']}
    for group in data:
        row = QtGui.QStandardItem(group)
        for item in data.get(group):
            row.appendRow(QtGui.QStandardItem(item))
        model.appendRow(row)

    proxy = FlatProxyModel()
    proxy.setSourceModel(model)

    w = QtWidgets.QWidget()
    layout = QtWidgets.QHBoxLayout(w)
    tree_view = QtWidgets.QTreeView()
    tree_view.setModel(model)
    tree_view.expandAll()
    tree_view.header().hide()
    layout.addWidget(tree_view)
    list_view = QtWidgets.QListView()
    list_view.setModel(proxy)
    layout.addWidget(list_view)
    w.show()

    sys.exit(app.exec_())
