# coding=utf8
# Copyright (c) 2018 CineUse

from Qt import QtGui
from Qt import QtWidgets
from Qt import QtCore


def get_file_icon(file_):
    file_ = file_.split(" ")[0]
    file_ = file_.strip()
    if file_:
        # convert file to image
        if filter(file_.lower().endswith, [".png", ".jpg", ".jpeg"]):
            pixmap = QtGui.QPixmap(file_).scaled(150, 150, QtCore.Qt.KeepAspectRatio)
        else:
            file_info = QtCore.QFileInfo(file_)
            icon_provider = QtWidgets.QFileIconProvider()
            icon = icon_provider.icon(file_info)
            pixmap = icon.pixmap(200, 200).scaled(100, 100, QtCore.Qt.KeepAspectRatio)
        return pixmap
