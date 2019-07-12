# coding=utf8
# Copyright (c) 2018 CineUse
from Qt import QtWidgets
from Qt import QtGui
from Qt import QtCore


class MultiComboBox(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super(MultiComboBox, self).__init__(parent)
        self.setModel(QtGui.QStandardItemModel(self))
        self.setEditable(True)

        self.lineEdit().setReadOnly(True)

        self.activated.connect(self.clear_selected)
        self.view().pressed.connect(self.handle_item_pressed)
        self.currentIndexChanged.connect(self.update_check)

    def clear_selected(self, *args, **kwargs):
        self.setCurrentIndex(-1)

    def clear(self):
        for row in range(self.count()):
            index = self.model().index(row, 0)
            item = self.model().itemFromIndex(index)
            item.setCheckState(QtCore.Qt.Unchecked)

    def update_check(self):
        checked_item_list = []
        for row in range(self.count()):
            index = self.model().index(row, 0)
            item = self.model().itemFromIndex(index)
            item.setCheckState(item.checkState())
            #
            if item.checkState() == QtCore.Qt.Checked:
                checked_item_list.append(item.text())

        self.lineEdit().setText(";".join(checked_item_list))

    def handle_item_pressed(self, index):
        # change check state
        item = self.model().itemFromIndex(index)
        if item.checkState() == QtCore.Qt.Checked:
            item.setCheckState(QtCore.Qt.Unchecked)
        else:
            item.setCheckState(QtCore.Qt.Checked)

    def checked_index(self):
        checked_index_list = []
        for row in range(self.count()):
            index = self.model().index(row, 0)
            item = self.model().itemFromIndex(index)
            if item.checkState() == QtCore.Qt.Checked:
                checked_index_list.append(row)
        return checked_index_list

    def checked_text(self):
        return self.lineEdit().text()

    def set_checked_index(self, index_list):
        self.clear()
        for row in index_list:
            index = self.model().index(row, 0)
            item = self.model().itemFromIndex(index)
            if item:
                item.setCheckState(QtCore.Qt.Checked)
        self.update_check()

    def set_checked_text(self, checked_text):
        self.clear()
        index_list = self.text_to_index(checked_text)
        self.set_checked_index(index_list)
        self.update_check()

    def text_to_index(self, text):
        text_list = text.split(";")
        index_list = []
        for text in text_list:
            row = self.findText(text)
            if row:
                index_list.append(row)
        return index_list


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    wgt = MultiComboBox()
    wgt.addItems(["hello", "world", "...", "1234"])
    wgt.update_check()
    wgt.show()
    app.exec_()
