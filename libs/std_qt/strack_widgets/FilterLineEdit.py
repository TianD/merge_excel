# coding=utf8
# Copyright (c) 2018 CineUse

import sys
import Qt.QtGui as QtGui
import Qt.QtCore as QtCore
from Qt import QtCompat
import logging


log = logging.getLogger('strack_client')

if "PySide" not in QtCompat.__binding__:
    QtCore.Slot = QtCore.pyqtSlot


class FilterLineEdit(QtGui.QLineEdit):
    def __init__(self, parent=None):
        super(FilterLineEdit, self).__init__(parent)


if __name__ == "__main__":
    FilterLineEdit()
