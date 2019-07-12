# coding:utf-8
import os
import sys
import codecs
import traceback

import pandas as pd

from Qt import QtWidgets
from Qt import QtGui
from Qt import QtCore

import std_qt
from AdditionTableModel import AdditionTableModel, MatchedColumnDelegate, AdditionColumnDelegate
from ResultTableModel import ResultTableModel

current_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.dirname(current_dir))
UI = os.path.join(current_dir, "MergeExcelWidget.ui")
FormClass, BaseClass = std_qt.load_ui_type(UI)


class MergeExcelWidget(FormClass, BaseClass):

    def __init__(self, parent=None):
        super(MergeExcelWidget, self).__init__(parent)

        self.__source_data = pd.DataFrame()

        self.setupUi(self)

        self.bind_fun()

    @property
    def source_data(self):
        return self.__source_data

    @source_data.setter
    def source_data(self, value):
        if isinstance(value, pd.DataFrame):
            self.__source_data = value
        else:
            raise TypeError('expected a pd.DataFrame object, but got a %s object.' % type(value).__name__)

    def setupUi(self, parent):
        super(MergeExcelWidget, self).setupUi(parent)
        self.addition_table_model = AdditionTableModel()
        self.addition_table_view.setModel(self.addition_table_model)
        self.addition_table_match_column_delegate = MatchedColumnDelegate(self)
        self.addition_table_view.setItemDelegateForColumn(1, self.addition_table_match_column_delegate)
        self.addition_table_addition_column_delegate = AdditionColumnDelegate(self)
        self.addition_table_view.setItemDelegateForColumn(2, self.addition_table_addition_column_delegate)

    def bind_fun(self):
        self.source_browse_btn.clicked.connect(self.edit_source_line_edit)
        self.export_browse_btn.clicked.connect(self.edit_export_line_edit)
        self.source_line_edit.textChanged.connect(self.init_source_data)
        self.add_btn.clicked.connect(self.add_addition_excel)
        self.del_btn.clicked.connect(self.del_addition_excel)
        self.addition_table_model.dataChanged.connect(self.update_source_data)
        self.base_column_combo_box.currentIndexChanged.connect(self.rematch_result_data)
        self.export_btn.clicked.connect(self.export)

    def edit_source_line_edit(self):
        excel_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, filter='*.xls *.xlsx')
        self.source_line_edit.setText(excel_path)

    def init_source_data(self, excel_path):
        self.result_data = pd.DataFrame()
        if os.path.isfile(excel_path):
            self.source_data = pd.read_excel(excel_path, sheet_name=0)
            self.result_data = self.result_data.append(self.source_data, ignore_index=True)
            self.refresh_result_data()
            self.base_column_combo_box.addItems(self.source_data.columns.values.tolist())
            self.base_column_combo_box.setCurrentIndex(0)

    def update_source_data(self, index1, index2):
        model = index1.model()
        self.result_data = pd.DataFrame()
        self.result_data = self.result_data.append(self.source_data, ignore_index=True)
        for row in range(model.rowCount()):
            match_column_data = model.source_data[row][1]
            addition_excel_path = model.source_data[row][0]
            addition_column_data = model.source_data[row][2]
            addition_excel_data = pd.read_excel(addition_excel_path, sheet_name=0)
            source_base_column = getattr(self.source_data, self.base_column_combo_box.currentText())
            if addition_column_data != '':
                for addition_column in addition_column_data.split(';'):
                    self.result_data[addition_column] = source_base_column.apply(lambda x: self._match_value(x, addition_excel_data, match_column_data, addition_column))
        self.refresh_result_data()

    def refresh_result_data(self):
        self.result_table_model = ResultTableModel(self.result_data)
        self.result_table_view.setModel(self.result_table_model)

    def rematch_result_data(self):
        pass

    def add_addition_excel(self):
        excel_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, filter='*.xls *.xlsx')
        if os.path.isfile(excel_path):
            self.addition_table_model.appendRow([excel_path, '', ''])

    def edit_export_line_edit(self):
        export_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, filter='.xls .xlsx')
        self.export_line_edit.setText(export_path)

    def export(self):
        export_path = self.export_line_edit.text()
        try:
            self.result_data.to_excel(export_path)
        except:
            QtWidgets.QMessageBox.error(self, 'Error', u'导出excel失败.')
            return
        QtWidgets.QMessageBox.information(self, 'Successfully', u'导出成功.')

    def del_addition_excel(self):
        selected_indexs = self.addition_table_view.selectedIndexes()
        for index in sorted(selected_indexs, key=lambda x: x.row())[::-1]:
            self.addition_table_model.removeRow(index.row())

    def _match_value(self, x, addition_excel_data, match_column_data, addition_column):
        try:
            if addition_excel_data[addition_excel_data[match_column_data] == x].values.tolist():
                return addition_excel_data[addition_excel_data[match_column_data] == x][addition_column].values.tolist()[0]
        except:
            return


def main():
    app = QtWidgets.QApplication(sys.argv)
    wgt = MergeExcelWidget()
    wgt.show()
    app.exec_()


if __name__ == '__main__':
    main()
