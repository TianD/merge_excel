# coding=utf8
# Copyright (c) 2018 CineUse

from Qt import QtCore
from Qt import QtGui
from Qt import QtWidgets

from strack_globals import StrackGlobals
from std_qt import strack_overlay


class ItemTreeView(QtWidgets.QTreeView):
    group_signal = QtCore.Signal(str)

    def __init__(self, parent=None):
        super(ItemTreeView, self).__init__(parent)

        self.init_items = None
        self.select_thread = None
        self.item_model = None
        self.item_delegate = None

        self.my_item_list = []
        if StrackGlobals.engine in ["maya", "nuke"]:
            style = "dark"
        else:
            style = "light"
        self.over_lay = strack_overlay.StrackOverlayWidget(self, style)

        self.header().hide()

    def update_view(self, lazy=False):
        if not self.select_thread:
            return
        self.over_lay.start_spin()
        if self.select_thread.isRunning():
            self.select_thread.quit()
        self.item_model.clear()
        self.clearSelection()
        self.select_thread.init_items = lambda: self.init_items(lazy=lazy)
        self.select_thread.start()

    def closeEvent(self, event):
        if self.select_thread and self.select_thread.isRunning():
            self.select_thread.terminate()
        event.accept()

    def mousePressEvent(self, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.LeftButton:
                super(ItemTreeView, self).mousePressEvent(event)
