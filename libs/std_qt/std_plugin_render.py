# coding=utf8
# Copyright (c) 2018 CineUse

from render_gui import render_gui
from strack_dialog.StrackBaseUI import StrackBaseUI
from load_ui_type import load_ui_type


def render(widget, app=None, style=None):
    return render_gui(StrackBaseUI, kwargs={"widget": widget}, app=app, style=style, singleton=False)


if __name__ == "__main__":
    from Qt import QtWidgets

    app = QtWidgets.QApplication([])

    UI = r"E:\temp\test.ui"
    FormClass, BaseClass = load_ui_type(UI)


    class TestUI(FormClass, BaseClass):
        def __init__(self):
            super(TestUI, self).__init__()

            self.setupUi(self)

    render(TestUI(), app)
