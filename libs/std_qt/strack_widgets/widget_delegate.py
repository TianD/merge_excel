# coding=utf8
# Copyright (c) 2018 CineUse

import weakref

import Qt
from Qt import QtCore
from Qt import QtWidgets


class WidgetDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, view):

        QtWidgets.QStyledItemDelegate.__init__(self, view)

        self.__paint_widget = None

        self.__editors = []

    @property
    def view(self):
        return self.parent()

    def _get_painter_widget(self, model_index, parent):

        if not model_index.isValid():
            return None

        if not self.__paint_widget or not self.__paint_widget():
            paint_widget = self._create_widget(parent)
            if not paint_widget:
                return None
            self.__paint_widget = weakref.ref(paint_widget)
        return self.__paint_widget()

    def _create_editor_widget(self, model_index, style_options, parent):
        if model_index.isValid():
            return self._create_widget(parent)

        return None

    def _on_before_paint(self, widget, model_index, style_options):
        """ virtual method """
        raise NotImplementedError

    def _create_widget(self, parent):
        """ virtual method """
        return None

    def createEditor(self, parent_widget, style_options, model_index):
        # allow derived class to create the editor widget:
        editor_widget = self._create_editor_widget(model_index, style_options, parent_widget)
        if not editor_widget:
            return None

        self.__editors.append(editor_widget)

        return editor_widget

    def updateEditorGeometry(self, editor_widget, style_options, model_index):
        editor_widget.setGeometry(style_options.rect)

    def paint(self, painter, style_options, model_index):

        # for performance reasons, we are not creating a widget every time
        # but merely moving the same widget around. 
        paint_widget = self._get_painter_widget(model_index, self.parent())
        if not paint_widget:
            # just paint using the base implementation:
            QtWidgets.QStyledItemDelegate.paint(self, painter, style_options, model_index)
            return

        # make sure that the widget that is just used for painting isn't visible otherwise
        # it'll appear in the wrong place!
        paint_widget.setVisible(False)

        # call out to have the widget set the right values            
        self._on_before_paint(paint_widget, model_index, style_options)

        # do paint
        painter.save()
        try:
            paint_widget.resize(style_options.rect.size())
            painter.translate(style_options.rect.topLeft())
            if Qt.__binding__ in ['PySide', 'PySide2']:
                paint_widget.render(painter,
                                    QtCore.QPoint(0, 0),
                                    renderFlags=QtWidgets.QWidget.DrawChildren)
            else :
                paint_widget.render(painter,
                                    QtCore.QPoint(0, 0),
                                    flags=QtWidgets.QWidget.DrawChildren)
        finally:
            painter.restore()
