# coding=utf8
# Copyright (c) 2018 CineUse

from functools import partial


def generate_menu(view_menu, item_info, parent):
    for menu in view_menu.item_list:
        menu_code = menu.get('code')
        menu_name = menu.get('name')
        menu_item_command = view_menu.execute_item
        setattr(parent, '%s_action' % menu_code, parent.root_menu.addAction(menu_name))
        action = getattr(parent, '%s_action' % menu_code)
        action.triggered.connect(partial(menu_item_command, menu_code, item_info, parent))
