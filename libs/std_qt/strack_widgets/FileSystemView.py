# coding=utf8
# Copyright (c) 2018 CineUse
import os

from Qt import QtCore
from Qt import QtGui
from Qt import QtWidgets


class FileSystemView(QtWidgets.QTreeView):

    def __init__(self, dir_path=QtCore.QDir.currentPath(), parent=None):
        super(FileSystemView, self).__init__(parent)

        self.dir_path = str(dir_path)
        self.item_model = QtWidgets.QFileSystemModel(self)
        self.setModel(self.item_model)

        self.item_model.setRootPath(self.dir_path)
        self.root_index = self.item_model.index(self.dir_path)
        self.setRootIndex(self.root_index)

    def update_view(self):
        self.item_model = QtWidgets.QFileSystemModel(self)
        self.setModel(self.item_model)
        self.item_model.setRootPath(self.dir_path)
        self.root_index = self.item_model.index(self.dir_path)
        self.setRootIndex(self.root_index)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    a = FileSystemView('d:/LocalWork')
    a.dir_path = 'd:/'
    a.show()
    # a.update_view()
    app.exec_()
