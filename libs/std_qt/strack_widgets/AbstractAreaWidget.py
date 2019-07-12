# coding=utf8
# Copyright (c) 2019 CineUse

from Qt import QtCore
from Qt import QtWidgets
from Qt import QtGui
from std_config.get_tool_config import get_tool_config


class AbstractAreaWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(AbstractAreaWidget, self).__init__(parent)

        self.config_name = ''
        self.sub_widgets = []
        self.tool_config = None

    def setup_config(self, config_name):
        self.config_name = config_name
        if not self.config_name:
            return
        self.tool_config = get_tool_config(self.config_name)
        if not self.tool_config:
            return

    def init_ui(self):
        pass

    def setup_sub_widgets(self):
        """
        Abstract
        :return:
        """
        pass

    def update_view(self, lazy=False):
        map(lambda x: x.update_view(lazy=lazy), self.sub_widgets)

    def clear_sub_widgets(self):
        for sub_widget in self.sub_widgets:
            sub_widget.close()
        self.sub_widgets = []
