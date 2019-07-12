# coding=utf8
# Copyright (c) 2018 CineUse


def setup_dict_combobox(combo, item_dict):
    combo.clear()
    for key, value in item_dict.items():
        combo.addItem(key, value)
