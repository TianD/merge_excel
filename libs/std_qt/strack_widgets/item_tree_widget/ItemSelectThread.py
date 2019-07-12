# coding=utf8
# Copyright (c) 2018 CineUse
import os
from Qt import QtCore
from std_config.get_bin_dir import get_bin_dir
from std_strack.cache_icon import cache_icon
from strack_globals import StrackGlobals


class ItemSelectThread(QtCore.QThread):
    got_item_list = QtCore.Signal(list)

    def __init__(self, select_function, default_icon_file):
        """
        create a thread for item select of a ItemTreeWidget.
        you must transfer a select function to emit the git_item_list signore.
        Args:
            select_function: callable
        """
        super(ItemSelectThread, self).__init__()
        self.__init_items = select_function
        self.default_icon_file = default_icon_file

    @property
    def init_items(self):
        return self.__init_items

    @init_items.setter
    def init_items(self, function):
        if not callable(function):
            error = TypeError(
                'ItemSelectThread.init_items must be callable, but %s type object got.' % type(function).__name__)
            raise error
        self.__init_items = function

    def run(self):
        # get items
        item_info_list = self.init_items() or []
        dam = StrackGlobals.dam
        creator_id_list = map(lambda x: x.get('created_by'), item_info_list)
        creator_info_list = dam.find('user', [['id', 'in', creator_id_list]])

        for item_info in item_info_list:
            # download icons
            thumb_location = cache_icon(dam, item_info)
            if not thumb_location:
                thumb_location = os.path.join(get_bin_dir(), 'images', self.default_icon_file)
            item_info.setdefault('thumb_location', thumb_location)

            # fill creator info
            if item_info.get('created_by'):
                item_info.setdefault('creator', next((i for i in creator_info_list
                                                      if i.get('id') == item_info.get('created_by')), {}))
            else:
                item_info.setdefault('creator', {})
        self.got_item_list.emit(item_info_list)
