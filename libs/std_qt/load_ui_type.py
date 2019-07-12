# coding=utf8
# Copyright (c) 2018 CineUse

import Qt.QtWidgets as QtWidgets
import Qt
import xml.etree.ElementTree as xml
from cStringIO import StringIO


def load_ui_type(ui_file):
    if "PySide" in Qt.__binding__:
        if Qt.__binding__ == "PySide2":
            import pyside2uic as pysideuic
        else:
            import pysideuic
        parsed = xml.parse(ui_file)
        widget_class = parsed.find('widget').get('class')
        form_class = parsed.find('class').text

        with open(ui_file, 'r') as f:
            o = StringIO()
            frame = {}

            pysideuic.compileUi(f, o, indent=0)
            pyc = compile(o.getvalue(), '<string>', 'exec')
            exec pyc in frame

            # Fetch the base_class and form class based on their type in the xml from designer
            form_class = frame['Ui_%s' % form_class]
            base_class = getattr(QtWidgets, widget_class)
        return form_class, base_class
    elif Qt.__binding__ == "PyQt4":
        import PyQt4.uic
        return PyQt4.uic.loadUiType(ui_file)


if __name__ == "__main__":
    pass
