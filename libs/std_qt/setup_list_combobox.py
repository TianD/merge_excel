# coding=utf8
# Copyright (c) 2018 CineUse


def setup_list_combobox(combo, item_list, show_key='name'):
    combo.clear()
    for item_info in item_list:
        if isinstance(item_info, dict):
            combo.addItem(item_info.get(show_key), item_info)
        else:
            pass
