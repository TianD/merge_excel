# coding=utf8
# Copyright (c) 2018 CineUse

from Qt import QtCore


def load_qss(file_path):
    css_file = QtCore.QFile(file_path)
    try:
        css_file.open(QtCore.QFile.ReadOnly)
        style_sheet = unicode(css_file.readAll(), encoding='utf8')
        return style_sheet
    finally:
        css_file.close()
