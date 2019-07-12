# coding=utf8
# Copyright (c) 2018 CineUse

import Qt
from Qt import QtCore


class ItemListModel(QtCore.QAbstractListModel):
    def __init__(self):
        super(ItemListModel, self).__init__()

        self.__item_list = []

    @property
    def item_list(self):
        return self.__item_list

    @item_list.setter
    def item_list(self, value):
        if isinstance(value, (list, tuple, set)):
            self.__item_list = value
            self.update_item_list(self.__item_list)
        else:
            raise TypeError(
                "The type of item_list's value should be one of list, tuple or set. \n\
                But got a %s value." % type(value).__name__)

    def pop_item(self, index):
        self.__item_list.pop(index.row())
        self.update_item_list(self.__item_list)

    def rowCount(self, *args, **kwargs):
        return len(self.__item_list)

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            return self.__item_list[row]

    def is_highlighted(self, index):
        return False

    def update_item_list(self, item_list):
        self.__item_list = item_list
        self.dataChanged.emit(self.index(0), self.index(len(self.__item_list) - 1))

    def item_data(self, index):
        return self.__item_list[index.row()]
