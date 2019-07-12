# coding=utf8
# Copyright (c) 2018 CineUse

from Qt import QtCore
from Node import Node


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


class MetadataItemModel(QtCore.QAbstractItemModel):
    def __init__(self, data_list=None, headers=None, parent=None):
        super(MetadataItemModel, self).__init__(parent)

        self.__origin_root_node = self.root_node = Node('root')
        self.data_list = data_list
        self.__column_headers = headers or data_list[0].keys()
        self.__groups = []

    @property
    def data_list(self):
        return self.__data_list

    @data_list.setter
    def data_list(self, value):
        if not isinstance(value, (list, tuple, set)):
            raise TypeError(
                "The type of item_list's value should be one of list, tuple or set. \
                But got a %s value." % value.__class__)
        self.__data_list = list(value)
        for data in self.__data_list:
            MetadataItemNode(data, self.root_node)

    @property
    def column_headers(self):
        return self.__column_headers

    @column_headers.setter
    def column_headers(self, value):
        if isinstance(value, (list, tuple, set)):
            self.__column_headers = list(value)
        else:
            raise TypeError(
                "The type of item_list's value should be one of list, tuple or set. \
                But got a %s value." % value.__class__)

    def rowCount(self, parent):
        parent_node = self.getNode(parent)
        return parent_node.childCount()

    def columnCount(self, *args, **kwargs):
        try:
            return len(self.__data_list[0].keys())
        except Exception:
            return 1

    def do_group(self, group_field):
        if group_field:
            self.group_items(group_field)
        else:
            self.ungroup_items()
        # self.layoutChanged.emit()

    def ungroup_items(self):
        self.beginInsertRows(QtCore.QModelIndex(), 0, 0)
        self.root_node = self.__origin_root_node
        self.endInsertRows()

    def group_items(self, group_field):
        # make group nodes
        self.beginInsertRows(QtCore.QModelIndex(), 0, 0)
        self.root_node = Node('grouped_root')
        self.__groups, grouped_data_list = self.group_data(self.data_list, group_field)
        for i, group in enumerate(self.__groups):
            group_node = Node(group, self.root_node)
            for data in grouped_data_list[i]:
                MetadataItemNode(data, group_node)
        self.endInsertRows()

    @staticmethod
    def group_data(data_list, group_field):
        groups = set(map(lambda data: data.get(group_field), data_list))
        grouped_data_list = [[data for data in data_list if data.get(group_field) == group_value]
                             for group_value in groups]
        return groups, grouped_data_list

    def data(self, index, role=QtCore.Qt.DisplayRole):
        col = index.column()
        header = self.column_headers[col]
        node = index.internalPointer()
        if role == QtCore.Qt.DisplayRole:
            if isinstance(node, MetadataItemNode):
                return node.meta_data.get(header)
            else:
                if col == 0:
                    return node.name()

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return self.__column_headers[section]

    def parent(self, index):
        node = self.getNode(index)
        parent_node = node.parent()
        if parent_node == self.root_node:
            return QtCore.QModelIndex()
        return self.createIndex(parent_node.row(), 0, parent_node)

    def index(self, row, column=1, parent=QtCore.QModelIndex()):
        parent_node = self.getNode(parent)
        child_item = parent_node.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QtCore.QModelIndex()

    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
        return self.root_node

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def removeRow(self, row, parent=QtCore.QModelIndex()):
        parent_node = parent.internalPointer()
        if parent_node:
            child_index = parent.child(row, 0)
        else:
            child_index = self.index(row, 0)
        node = child_index.internalPointer()
        meta_data = node.meta_data
        self.item_list = filter(lambda item: item.get("name") != meta_data.get("name"), self.__item_list)
        return super(MetadataItemModel, self).removeRow(row, child_index.parent())
