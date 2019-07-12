# coding=utf8
# Copyright (c) 2018 CineUse
from Qt import QtCore
from Qt import QtWidgets
from Qt import QtGui


class IconItemList(QtWidgets.QListWidget):
    addfile = QtCore.Signal(str)
    dropped = QtCore.Signal(int, int)
    item_insert = QtCore.Signal(list)
    item_deleted = QtCore.Signal(list)
    item_edit = QtCore.Signal(list)
    _rows_to_del = []

    def __init__(self, parent=None, size=64, size_buffer=12, deleteable=False):
        super(IconItemList, self).__init__(parent)

        self.menu = QtWidgets.QMenu(self)

        self.setIconSize(QtCore.QSize(size, size))
        self.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.setGridSize(QtCore.QSize(size + size_buffer, size + size_buffer))
        self.setDragEnabled(True)

        self.setViewMode(QtWidgets.QListWidget.IconMode)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setAcceptDrops(True)

        self._dropping = False
        self.deleteable = deleteable
        self.setSelectionRectVisible(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            super(IconItemList, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            super(IconItemList, self).dragMoveEvent(event)

    def dropEvent(self, event):
        if event.source() is self:
            return
        else:
            event.setDropAction(QtCore.Qt.CopyAction)
        self._dropping = True
        super(IconItemList, self).dropEvent(event)
        self._dropping = False
        self.item_insert.emit(self.dropped_items)

    def rowsInserted(self, parent, start, end):
        if self._dropping:
            self.dropped.emit(start, end)
        self.dropped_items = []
        for row in range(start, end + 1):
            self.dropped_items.append(self.item(row))

        super(IconItemList, self).rowsInserted(parent, start, end)

    def keyPressEvent(self, event):
        """ press delete to remove an item """
        if event.key() == QtCore.Qt.Key_Delete and self.deleteable:
            self.item_deleted.emit(self.selectedItems())
            for item in self.selectedItems():
                self.takeItem(self.row(item))

    def contextMenuEvent(self, event):
        """ right clicked to popup menu"""
        pos = event.pos()
        item = self.itemAt(pos)
        if not item:
            return
        if not hasattr(item, 'handler'):
            return

        self.menu.clear()
        for action in item.handler.actions():
            if isinstance(action, QtWidgets.QAction):
                self.menu.addAction(action)
            elif isinstance(action, QtWidgets.QMenu):
                self.menu.addMenu(action)
        self.menu.popup(event.globalPos())


if __name__ == "__main__":
    IconItemList()
