# coding=utf8
# Copyright (c) 2018 CineUse

import os
import sys

from std_py.import_class import import_class
from std_qt import load_ui_type

current_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.dirname(current_dir))
UI = os.path.join(current_dir, "process_widget.ui")
FormClass, BaseClass = load_ui_type(UI)


class ProcessWidget(FormClass, BaseClass):

    def __init__(self, parent=None):
        super(ProcessWidget, self).__init__(parent)
        self.setupUi(self)
        self.__process = None

    @property
    def process(self):
        return self.__process

    def setup_process(self, category, config, context):
        format_name = "".join([part.capitalize() for part in category.split("_")])
        class_str = "std_pipeline.{0}Process.{0}Process".format(format_name)

        process_class = import_class(class_str)
        self.__process = process_class(config, context)

    def setup_manual_area(self, widget):
        self.manual_area.layout().addWidget(widget)
