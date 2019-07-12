# coding=utf8
# Copyright (c) 2017 CineUse


class Node(object):
    def __init__(self, name, parent=None):
        self._name = name
        self._children = list()
        self._parent = parent
        if parent:
            parent.append_child(self)

    def append_child(self, child):
        self._children.append(child)

    def name(self):
        return self._name

    def setName(self, name):
        self._name = name

    def child(self, row):
        if len(self._children) > row:
            return self._children[row]

    def children(self):
        return self._children

    def childCount(self):
        return len(self._children)

    def parent(self):
        return self._parent

    def row(self):
        if self._parent:
            return self._parent._children.index(self)
        else:
            return -1

    def isValid(self):
        return False

    def clear(self):
        self._children = list()

    def find(self, name):
        for i in self._children:
            if i.name() == name:
                return i

    def remove_child(self, row):
        try:
            self._children.pop(row)
            return True
        except:
            return False
