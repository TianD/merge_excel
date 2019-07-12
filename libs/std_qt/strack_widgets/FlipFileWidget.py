# coding=utf8
# Copyright (c) 2018 CineUse

from Qt import QtCore
from Qt import QtWidgets
from Qt import QtGui

from std_qt.strack_widgets.FileArea import FileArea


class FlipFileWidget(QtWidgets.QGroupBox):
    def __init__(self, parent=None):
        super(FlipFileWidget, self).__init__(parent)

        self.default_flag = True
        self.setupUi(self)

    def setupUi(self, parent):
        self.setMinimumHeight(200)
        self.main_layout = QtWidgets.QHBoxLayout(self)

        self.file_area = FileArea()
        self.main_layout.addWidget(self.file_area)

        self.flip_btn = QtWidgets.QToolButton()
        self.flip_btn.setStyleSheet('border:none')
        self.flip_btn.setIcon(QtGui.QIcon(':/icons/on.png'))
        self.flip_btn.setIconSize(QtCore.QSize(32, 32))
        self.main_layout.addWidget(self.flip_btn)

        self.main_layout.setStretch(0, 1)

        # set publish drop area
        self.file_area.ext_filters = ['*']
        self.file_area.multi_files = True

        self.flip_btn.clicked.connect(self.drop_change)

    def drop_change(self):
        if self.default_flag:
            self.file_area.accept_files_flag = False
            self.file_area.setText('Will be generated automatically by calling hook')
            self.file_area.setEnabled(False)
            self.flip_btn.setIcon(QtGui.QIcon(':/icons/off.png'))
            self.default_flag = False
            self.flip_btn.setChecked(False)
        else:
            self.file_area.accept_files_flag = True
            self.file_area.setText('Drag and drop files here or click to browse')
            self.file_area.setEnabled(True)
            self.flip_btn.setIcon(QtGui.QIcon(':/icons/on.png'))
            self.default_flag = True
            self.flip_btn.setChecked(True)

    def setShown(self, flag):
        if flag == QtCore.Qt.Checked:
            self.setHidden(False)
        else:
            self.setHidden(True)
