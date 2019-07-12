# coding=utf8
# Copyright (c) 2018 CineUse
import os
import sys
import HTMLParser

from Qt import QtWidgets
from Qt import QtGui
from Qt import QtCore
from ..load_ui_type import load_ui_type
from std_qt.create_round_image import create_round_image

current_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.dirname(current_dir))
UI = os.path.join(current_dir, "note_widget.ui")
FormClass, BaseClass = load_ui_type(UI)


class NoteWidget(FormClass, BaseClass):

    def __init__(self, parent=None):
        super(NoteWidget, self).__init__(parent)

        self.setupUi(self)

    def set_user_icon(self, user_icon_path):
        icon_image = create_round_image(user_icon_path)
        self.user_icon.setPixmap(icon_image)

    def set_current_note_label(self, data):
        self.current_note_label.setText(data)

    def set_parent_note_label(self, data):
        self.parent_note_label.setText(data)

    def set_note_text(self, data):
        html_parser = HTMLParser.HTMLParser()
        txt = html_parser.unescape(data)
        self.text_widget.setHtml(txt)

    def set_note_media(self, media_list):
        self.media_widget.clear()
        for media_path in media_list:
            item = QtWidgets.QListWidgetItem()
            pixmap = QtGui.QPixmap(media_path)
            if pixmap.isNull():
                continue
            item_icon = QtGui.QIcon(pixmap)
            item.setIcon(item_icon)
            self.media_widget.addItem(item)

    @staticmethod
    def calculate_size():
        return QtCore.QSize(355, 200)
