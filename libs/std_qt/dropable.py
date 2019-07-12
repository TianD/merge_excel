# coding=utf8
# Copyright (c) 2018 CineUse

import Qt
from Qt import QtWidgets
from Qt import QtGui
from Qt import QtCore
import logging


log = logging.getLogger('strack_client')


def dropable(widget):
    class Filter(QtCore.QObject):
        drop_in = QtCore.Signal(list)

        def eventFilter(self, obj, event):

            if obj == widget:
                if event.type() in [QtCore.QEvent.DragEnter, QtCore.QEvent.DragMove]:
                    if event.mimeData().hasUrls():
                        event.acceptProposedAction()
                        return True
                    else:
                        event.ignore()
                        return False
                if event.type() == QtCore.QEvent.Drop:
                    in_paths = []
                    for url in event.mimeData().urls():
                        path = url.toLocalFile()
                        in_paths.append(path)
                    self.drop_in.emit(in_paths)
                    return True
            return False

    if hasattr(widget, "setAcceptDrops"):
        widget.setAcceptDrops(True)
    obj = Filter(widget)
    widget.installEventFilter(obj)
    return obj.drop_in


if __name__ == "__main__":
    import sys

    class TestWidget(QtWidgets.QDialog):
        """Load .ui file example, using setattr/getattr approach"""
        def __init__(self, parent=None):
            QtWidgets.QDialog.__init__(self, parent)
            self.layout = QtWidgets.QVBoxLayout(self)
            self.tree = QtWidgets.QTreeView()
            self.layout.addWidget(self.tree)
            dropped = dropable(self.tree)
            dropped.connect(self.on_drop)

        def on_drop(self, files):
            print files

    app = QtWidgets.QApplication(sys.argv)
    wgt = TestWidget()

    wgt.show()
    app.exec_()
    pass
