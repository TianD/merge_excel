# coding=utf8
# Copyright (c) 2018 CineUse

import os.path

from Qt import QtWidgets
from Qt import QtGui

from load_style import load_style
from StrackColorScheme import StrackColorScheme

QSS_DIR = os.path.join(os.path.dirname(__file__), "styles")

COLOR_SCHEME_DICT = {
    "dark": {
        "baseColor": QtGui.QColor(50, 50, 50),
        "highlightColor": QtGui.QColor(247, 147, 30),
        "spread": 2.5
    },
    "light": {
        "baseColor": QtGui.QColor("#eee"),
        "highlightColor": QtGui.QColor("58B7FF"),
        "spread": 2.5
    },
    "default": {
        "baseColor": QtGui.QColor("#f7f7f7"),
        # "highlightColor": QtGui.QColor("#ace5ff"),
        "highlightColor": QtGui.QColor("#20A0FF"),
        "spread": 2.5
    }
}


def set_style_scheme(gui_obj, style="", color_scheme=""):
    qss_name = r"%s/%s.qss" % (QSS_DIR, style)
    if not os.path.isfile(qss_name):
        qss_name = r"%s/%s.qss" % (QSS_DIR, "default")
    stylesheet = load_style(qss_name)
    if isinstance(gui_obj, QtWidgets.QWidget):
        gui_obj.setStyleSheet(stylesheet)
    if color_scheme in COLOR_SCHEME_DICT:
        StrackColorScheme(**COLOR_SCHEME_DICT.get(color_scheme))
