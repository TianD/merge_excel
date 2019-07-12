# coding=utf8
# Copyright (c) 2018 CineUse
import os
import logging
import clique
from Qt import QtCore, QtWidgets, QtGui

log = logging.getLogger('strack_client')


class FileArea(QtWidgets.QLabel):
    file_selected = QtCore.Signal(str, str)

    def __init__(self, parent=None):
        super(FileArea, self).__init__(parent)

        self.__ext_list = []
        self.root_dir = ""
        self.setAcceptDrops(True)
        self.setText("Drop your files or clicked to select.")
        self.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        # style
        self.setStyleSheet('''QLabel{
                padding:3px;
                width:70px;
                height:15px;
                border: 2px dotted #999;
                border-radius: 10px;
                font: bold 12px/25px Arial, sans-serif;
                color: #999;
            }
            QLabel:hover{
                border-color: #2194c4;
                color:  #2194c4;
            }''')

    def set_ext_list(self, ext_list):
        self.__ext_list = ext_list

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            # open a file browser dialog
            filter_str = " ".join(["*%s" % i for i in self.__ext_list])
            file_list, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Select File",
                                                                  self.root_dir, "Files (%s)" % filter_str)

            collections, remainders = clique.assemble(file_list, patterns=[clique.PATTERNS['frames']])
            if collections:
                code, file_path = self._validate_collection(collections[0])
                self.file_selected.emit(code, file_path)
                return

            if remainders:
                code, file_path = self._validate_remainder(remainders[0])
                self.file_selected.emit(code, file_path)
                return

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        file_list = [url.toLocalFile() for url in event.mimeData().urls()]
        collections, remainders = clique.assemble(file_list, patterns=[clique.PATTERNS['frames']])
        if collections:
            code, file_path = self._validate_collection(collections[0])
            self.file_selected.emit(code, file_path)
            return

        if remainders:
            code, file_path = self._validate_remainder(remainders[0])
            self.file_selected.emit(code, file_path)
            return

    def _validate_collection(self, collection):
        code = os.path.basename(collection.head[:-1])
        return code, collection.format()

    def _validate_remainder(self, remainder):
        code, ext = os.path.splitext(os.path.basename(remainder))
        return code, remainder


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    test = FileArea()
    test.show()
    app.exec_()
