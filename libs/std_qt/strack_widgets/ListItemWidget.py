# coding=utf8
# Copyright (c) 2018 CineUse
import sys
import os
from Qt import QtWidgets
from Qt import QtCore
from Qt import QtGui
import std_qt

current_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.dirname(current_dir))
UI = os.path.join(current_dir, "list_item_widget.ui")
FormClass, BaseClass = std_qt.load_ui_type(UI)


class ListItemWidget(FormClass, BaseClass):
    """
    Widget that is used to display entries in all the item listings.
    This widget goes together with the list item delegate and is always
    manufactured by the list item delegate.
    """

    def __init__(self, parent):
        """
        Constructor

        :param parent: QT parent object
        """
        QtWidgets.QWidget.__init__(self, parent)

        # make sure this widget isn't shown
        self.setVisible(False)

        # set up the UI
        self.setupUi(self)

        self._css_decorated = """
            #box { border-width: 2px;
                   border-radius: 4px;
                   border-color: rgb(48, 167, 227);
                   border-style: solid;
            }
            """

        self._css_selected = """
            #box { border-width: 2px;
                   border-radius: 4px;
                   border-color: rgb(48, 167, 227);
                   border-style: solid;
                   background-color: rgba(48, 167, 227, 25%);
            }
            """

        self._no_style = """
            #box { border-width: 2px;
                   border-radius: 4px;
                   border-color: rgba(0, 0, 0, 0%);
                   border-style: solid;
            }
            """

    def set_selected(self, selected):
        if selected:
            self.box.setStyleSheet(self._css_selected)

    def set_highlighted(self, highlighted):
        if highlighted:
            self.box.setStyleSheet(self._css_decorated)
        else:
            self.box.setStyleSheet(self._no_style)

    def set_thumbnail(self, pixmap):
        pixmap = QtGui.QPixmap(pixmap)
        if pixmap.isNull():
            return
        pixmap = pixmap.scaled(125, 70)
        self.thumbnail.setPixmap(pixmap)

    def set_text(self, body):
        self.list_item_body.setText(body)

    @staticmethod
    def calculate_size():
        return QtCore.QSize(300, 108)


if __name__ == "__main__":
    ListItemWidget()
