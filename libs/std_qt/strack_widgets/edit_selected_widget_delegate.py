# coding=utf8
# Copyright (c) 2018 CineUse

from Qt import QtCore
from std_py.flat_item_info import flat_item_info
from widget_delegate import WidgetDelegate
from std_py.AdvFormatter import AdvFormatter
from std_qt.strack_models.TreeGroupModel import GroupItemNode
from std_qt.strack_widgets.ListItemWidget import ListItemWidget


class EditSelectedWidgetDelegate(WidgetDelegate):

    def __init__(self, body_html, view):
        super(EditSelectedWidgetDelegate, self).__init__(view)

        self.__view = view
        self.__body_html = body_html
        # tracks the currently active cell
        self.__current_editor_index = None

        # note! Need to have a model connected to the view in order
        # to have a selection model.
        self.selection_model = view.selectionModel()

        if self.selection_model:
            self.selection_model.selectionChanged.connect(self._on_selection_changed)

    @property
    def body_html(self):
        return self.__body_html

    @body_html.setter
    def body_html(self, value):
        if isinstance(value, basestring):
            self.__body_html = value
        else:
            raise TypeError("expected a string object, but got a %s object." % type(value).__name__)

    @property
    def view(self):
        return self.__view

    def _create_widget(self, parent):
        return ListItemWidget(parent)

    def _on_before_selection(self, widget, index, style_options):
        # do std drawing first
        self._on_before_paint(widget, index, style_options)
        node = index.internalPointer()
        if not isinstance(node, GroupItemNode):
            widget.set_selected(True)

    def _on_before_paint(self, widget, index, style_options):
        node = index.internalPointer()
        if isinstance(node, GroupItemNode):
            widget.set_text(u'<b>%s</b>' % node.name())
            widget.thumbnail.hide()
            return
        # note: This is a violation of the model/delegate independence.
        if index.model().is_highlighted(index):
            widget.set_highlighted(True)
        else:
            widget.set_highlighted(False)

        # get the item data
        item_info = index.data()

        # thumb
        thumb = item_info.get('thumb_location')
        if thumb:
            widget.set_thumbnail(thumb)

        fmt = AdvFormatter()
        body_info = fmt.format(self.__body_html, **flat_item_info(item_info))
        widget.set_text(body_info)

        if self.view.width() < 265:
            widget.thumbnail.hide()
        else:
            widget.thumbnail.show()

    def _on_selection_changed(self, selected, deselected):
        # clean up        
        if self.__current_editor_index:
            self.parent().closePersistentEditor(self.__current_editor_index)
            self.__current_editor_index = None

        selected_indexes = selected.indexes()

        if len(selected_indexes) > 0:
            # get the currently selected model index
            model_index = selected_indexes[0]
            # create an editor widget that we use for the selected item
            self.__current_editor_index = model_index
            # this will trigger the call to createEditor
            self.parent().openPersistentEditor(model_index)

    def createEditor(self, parent_widget, style_options, model_index):

        # create the editor by calling the base method:
        editor_widget = WidgetDelegate.createEditor(self, parent_widget, style_options, model_index)

        # and set it up to operate on the index:
        self._on_before_selection(editor_widget, model_index, style_options)
        return editor_widget

    def paint(self, painter, style_options, model_index):
        # if model_index == self.__current_editor_index:
        #     # avoid painting the index twice!
        #     return
        WidgetDelegate.paint(self, painter, style_options, model_index)

    def sizeHint(self, style_options, index):
        node = index.internalPointer()
        if isinstance(node, GroupItemNode):
            return QtCore.QSize(300, 30)
        return ListItemWidget.calculate_size()
