# coding=utf8

import os
import sys

import Qt.QtGui as QtGui
import Qt.QtWidgets as QtWidgets

from load_style import load_style
from StrackColorScheme import StrackColorScheme

QSS_DIR = os.path.join(os.path.dirname(__file__), "styles")


def render_gui(GUIClass, args=[], kwargs={}, app=None, style="default", color_scheme=None, singleton=False):
    # init event loop
    if not app:
        use_default_app = True
        app = QtWidgets.QApplication(sys.argv)
    else:
        use_default_app = False
    # init gui object
    gui_obj = GUIClass(*args, **kwargs)
    # # set stylesheet
    # qss_name = r"%s/%s.qss" % (QSS_DIR, style)
    # if not os.path.isfile(qss_name):
    #     qss_name = r"%s/%s.qss" % (QSS_DIR, "default")
    # stylesheet = load_style(qss_name)
    # if isinstance(gui_obj, QtWidgets.QWidget):
    #     gui_obj.setStyleSheet(stylesheet)
    # singleton
    if singleton:
        for widget in app.allWidgets():
            if gui_obj.objectName() == widget.objectName():
                widget.close()  # fixme: this will effect closeEvents
    # set Color Scheme
    color_scheme_dict = {
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
    # if color_scheme in color_scheme_dict:
    #     StrackColorScheme(**color_scheme_dict.get(color_scheme))
    # run gui
    gui_obj.show()
    # don't close after window closed
    QtWidgets.QApplication.setQuitOnLastWindowClosed(False)
    # run event loop
    if use_default_app:
        app.exec_()
    return gui_obj
