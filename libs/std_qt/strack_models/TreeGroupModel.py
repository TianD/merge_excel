# coding=utf8
# Copyright (c) 2018 CineUse

from Qt import QtCore

from Node import Node
from std_py.flat_item_info import flat_item_info


class GroupItemNode(Node):

    def __init__(self, name, parent=None):
        super(GroupItemNode, self).__init__(name, parent)


class MetadataItemNode(Node):

    def __init__(self, data, parent=None):
        name = data.get('name', 'NotNamed')
        super(MetadataItemNode, self).__init__(name, parent)
        self.__meta_data = data

    @property
    def meta_data(self):
        return self.__meta_data

    @meta_data.setter
    def meta_data(self, value):
        if isinstance(value, dict):
            self.__meta_data = value
        else:
            raise TypeError(
                "The type of item_list's value should be dict. \
                But got a %s value." % value.__class__)


class TreeGroupModel(QtCore.QAbstractItemModel):
    expand_signal = QtCore.Signal()

    def __init__(self, item_list=None, parent=None):
        super(TreeGroupModel, self).__init__(parent)
        self.__view = parent
        self.__origin_root_node = self.root_node = Node('root')
        self.item_list = item_list or []
        self.__groups = []

    @property
    def view(self):
        return self.__view

    @property
    def groups(self):
        return self.__groups

    @groups.setter
    def groups(self, value):
        self.__groups = value

    @property
    def item_list(self):
        return self.__item_list

    @item_list.setter
    def item_list(self, value):
        if not isinstance(value, (list, tuple, set)):
            raise TypeError(
                "The type of item_list's value should be one of list, tuple or set. \
                But got a %s value." % value.__class__)
        self.root_node.clear()
        self.__item_list = list(value)
        for data in self.__item_list:
            MetadataItemNode(data, self.root_node)

    def rowCount(self, parent):
        parent_node = self.getNode(parent)
        return parent_node.childCount()

    def columnCount(self, *args, **kwargs):
        return 1

    def do_group(self, group_field):
        self.view.clearSelection()
        if group_field:
            self.group_items(group_field)
        else:
            self.ungroup_items()

    def ungroup_items(self):
        self.beginInsertRows(QtCore.QModelIndex(), 0, 0)
        self.root_node = self.__origin_root_node
        self.endInsertRows()

    def group_items(self, group_field):
        # make group nodes
        self.beginInsertRows(QtCore.QModelIndex(), 0, 0)
        self.root_node = Node('grouped_root')
        self.groups, grouped_item_list = self.group_data(self.item_list, group_field)
        for i, group in enumerate(self.groups):
            group_node = GroupItemNode(group, self.root_node)
            for data in grouped_item_list[i]:
                MetadataItemNode(data, group_node)
        self.endInsertRows()
        self.expand_signal.emit()

    @staticmethod
    def group_data(item_list, group_field):
        groups = set(map(lambda x: flat_item_info(x).get(group_field), item_list))
        grouped_item_list = [[item for item in item_list if flat_item_info(item).get(group_field) == group_value]
                             for group_value in groups]
        return groups, grouped_item_list

    def data(self, index, role=QtCore.Qt.DisplayRole):
        col = index.column()
        node = index.internalPointer()
        if role == QtCore.Qt.DisplayRole:
            if isinstance(node, MetadataItemNode):
                return node.meta_data
            else:
                if col == 0:
                    return node.name()

    def parent(self, index):
        node = self.getNode(index)
        parent_node = node.parent()
        if not parent_node:
            return QtCore.QModelIndex()
        if parent_node == self.root_node:
            return QtCore.QModelIndex()
        return self.createIndex(parent_node.row(), 0, parent_node)

    def index(self, row, column=0, parent=QtCore.QModelIndex()):
        parent_node = self.getNode(parent)
        if not parent_node.children():
            return QtCore.QModelIndex()
        child_item = parent_node.child(row)
        return self.createIndex(row, column, child_item)

    def getNode(self, index):
        if index and index.isValid():
            node = index.internalPointer()
            if isinstance(node, Node):
                return node
        return self.root_node

    def flags(self, index):
        node = index.internalPointer()
        if isinstance(node, GroupItemNode):
            return QtCore.Qt.ItemIsEnabled
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def update_item_list(self, item_list):
        self.beginResetModel()
        self.item_list = item_list
        self.endResetModel()

    def clear(self):
        self.beginResetModel()
        self.item_list = []
        self.endResetModel()

    def is_highlighted(self, index):
        """abstract method"""
        return False

    def get_item_data(self, index):
        node = index.internalPointer()
        if isinstance(node, GroupItemNode):
            return node.name()
        return node.meta_data
