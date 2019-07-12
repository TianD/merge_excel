# coding=utf8
# Copyright (c) 2018 CineUse


def setup_combobox(combo_widget, string_list, default_item=None):
    combo_widget.blockSignals(True)
    combo_widget.clear()

    if string_list:
        combo_widget.addItems(string_list)

    current_index = combo_widget.currentIndex()
    if default_item is not None:
        index = combo_widget.findText(default_item)
        current_index = 0 if index == -1 else current_index

    combo_widget.blockSignals(False)
    combo_widget.setCurrentIndex(current_index)
