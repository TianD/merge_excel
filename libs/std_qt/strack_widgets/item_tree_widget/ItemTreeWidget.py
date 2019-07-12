# coding=utf8
# Copyright (c) 2018 CineUse
import os
import sys
from Qt import QtWidgets
from Qt import QtCore
from Qt import QtGui

import std_qt
from std_py.flat_item_info import flat_item_info
from std_qt.generate_menu import generate_menu
from std_qt.setup_combobox import setup_combobox
from std_qt.strack_models.TreeGroupModel import TreeGroupModel
from std_config.get_tool_config import get_tool_config
from std_strack.StrackMenu import StrackMenu

current_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.dirname(current_dir))
UI = os.path.join(current_dir, "item_tree_widget.ui")
FormClass, BaseClass = std_qt.load_ui_type(UI)


class ItemTreeWidget(FormClass, BaseClass):
    item_selected = QtCore.Signal(QtCore.QModelIndex)

    def __init__(self, parent=None):
        super(ItemTreeWidget, self).__init__(parent)

        self.setupUi(self)

        self.current_filter_field = ''
        self.current_filter_pattern = ''
        self.current_group_field = ''

        self.config_name = ''
        self.tool_config = None
        self.filter_fields = None
        self.group_fields = None
        self.module_code = None
        self.item_template = None
        self.body_html = None
        self.default_icon_file = None

        self.__tool_name = ''
        self.__header_list = []
        self.__filter_list = []
        self.__items_about_to_select = []
        self.my_item_list = []

        self.root_menu = None
        self.context_menu = None
        self.current_index_at = QtCore.QModelIndex()
        self.current_index = QtCore.QModelIndex()

        self.init_ui()

        self.bind_func()

    @property
    def tool_name(self):
        return self.__tool_name

    @tool_name.setter
    def tool_name(self, value):
        if isinstance(value, basestring):
            self.__tool_name = value
        else:
            raise TypeError('tool_name must be a string, %s object got.' % type(value).__name__)

    @property
    def header_list(self):
        return self.__header_list

    @header_list.setter
    def header_list(self, value):
        if isinstance(value, list):
            self.__header_list = value
        else:
            raise TypeError('header_list must be a list, %s object got.' % type(value).__name__)

    @property
    def filter_list(self):
        return self.__filter_list

    @filter_list.setter
    def filter_list(self, value):
        if not value:
            self.__filter_list = []
            return
        if isinstance(value, list) and isinstance(value[0], list):
            self.__filter_list = value
        else:
            raise TypeError('filter_list must be a list, %s object got.' % type(value).__name__)

    @property
    def items_about_to_select(self):
        return self.__items_about_to_select

    @items_about_to_select.setter
    def items_about_to_select(self, value):
        if not value:
            self.__items_about_to_select = []
            return
        if isinstance(value, list) and all(map(lambda x: isinstance(x, dict), value)):
            self.__items_about_to_select = value
        else:
            raise TypeError('items_about_to_select must be a list, %s object got.' % type(value).__name__)

    def bind_func(self):
        # connect signals to slots
        self.group_combo.currentIndexChanged[str].connect(self.item_view.group_signal)
        self.filter_combo.currentIndexChanged.connect(self.show_filter_items)
        self.filter_lineEdit.textChanged.connect(self.show_filter_items)
        self.item_view.group_signal.connect(self.item_view.item_model.do_group)
        self.item_view.item_model.expand_signal.connect(self.item_view.expandAll)
        self.item_view.customContextMenuRequested.connect(self.custom_menu)

    def setup_config(self, config_name):
        self.config_name = config_name
        if not self.config_name:
            return
        self.tool_config = get_tool_config('item_select_widget/%s' % self.config_name)
        if not self.tool_config:
            return
        self.filter_fields = self.tool_config.get('filter_fields')
        self.group_fields = self.tool_config.get('group_fields')
        self.module_code = self.tool_config.get('module')
        self.item_template = self.tool_config.get('item_template')
        self.default_icon_file = self.tool_config.get('icon_file')
        self.hide_widgets()

        self.item_view.init_items = self.init_items
        self.item_menu_config = self.tool_config.get('item_menus')
        self.view_menu_config = self.tool_config.get('view_menus')

    def hide_widgets(self):
        widgets_to_hide = self.tool_config.get('hide_widgets')
        for widget_name in widgets_to_hide:
            widget = self.findChild(QtWidgets.QWidget, widget_name)
            if widget:
                widget.hide()

    def show_filter_items(self):
        # fixme: current_group_field在没有调用当前方法的时候, 一直都会保持为初始值
        self.current_filter_pattern = self.filter_lineEdit.text()
        self.current_filter_field = self.filter_combo.currentText()
        self.current_group_field = self.group_combo.currentText()
        self.show_items(self.my_item_list)

    def init_ui(self):
        self.item_view.item_model = TreeGroupModel(parent=self.item_view)
        self.item_view.setModel(self.item_view.item_model)

        self.root_menu = QtWidgets.QMenu(self.item_view)

        self.context_menu = StrackMenu()
        self.item_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

    def custom_menu(self, point):
        self.root_menu.clear()
        self.current_index_at = self.item_view.indexAt(point)

        if self.current_index_at.isValid():
            item_info = self.item_view.item_model.get_item_data(self.current_index_at)
        else:
            item_info = None

        if self.current_index_at.isValid():
            # 如果选中了index, 则使用item menu
            self.context_menu.initialize(self.item_menu_config)
            generate_menu(self.context_menu, item_info, self)
        else:
            # 如果没有选中index, 则使用item menu
            self.context_menu.initialize(self.view_menu_config)
            generate_menu(self.context_menu, item_info, self)
        self.root_menu.exec_(QtGui.QCursor.pos())

    def select_item(self, index):
        self.item_selected.emit(index)

    def show_items(self, item_list=None):
        self.item_view.over_lay.hide()
        if item_list:
            self.my_item_list = item_list
            if self.current_filter_pattern:
                filter_item_list = filter(
                    lambda x: unicode(x.get(self.current_filter_field, "") or "").find(self.current_filter_pattern) >= 0,
                    self.my_item_list)
            else:
                filter_item_list = self.my_item_list
            self.item_view.item_model.update_item_list(filter_item_list)
            if self.current_group_field:
                self.item_view.clearSelection()
                self.item_view.item_model.ungroup_items()
                self.item_view.item_model.do_group(self.current_group_field)

            # select items
            for item_info in self.items_about_to_select:
                if item_info in self.item_view.item_model.item_list:
                    row = self.item_view.item_model.item_list.index(item_info)
                    qt_selection = QtCore.QItemSelection(self.item_view.item_model.index(row),
                                                         self.item_view.item_model.index(row,
                                                                                         len(self.header_list)))
                    self.item_view.selectionModel().select(qt_selection, QtCore.QItemSelectionModel.Select)

    def init_items(self, lazy=False):
        """
                Abstract method, you must overwrite this method to get items
                Returns:
                    list of dict, metadata of selected items.
                    metadata must include 'media', 'id', 'module' keys.
                """
        return []

    def update_view(self, lazy=False):
        setup_combobox(self.filter_combo, self.filter_fields, default_item=self.filter_fields[0])
        setup_combobox(self.group_combo, [""] + self.group_fields, default_item="")
        self.item_view.update_view(lazy=lazy)
