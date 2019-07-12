# coding=utf8
# Copyright (c) 2018 CineUse

import time

from Qt import QtCore
from Qt import QtWidgets


class TimerLabel(QtWidgets.QLabel):
    on_start = QtCore.Signal()
    on_stop = QtCore.Signal()

    def __init__(self, parent=None):
        super(TimerLabel, self).__init__(parent)
        self.__used_time = 0
        self.__start_time = None
        self._time_template = "%Y-%m-%d %H:%M:%S"

        self._current_times = 0
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.show_time)

    @property
    def is_active(self):
        return self._timer.isActive()

    @property
    def used_time(self):
        return self.__used_time

    @used_time.setter
    def used_time(self, value):
        self.__used_time = self.check_time_format(value)

    @property
    def start_time(self):
        return self.__start_time

    @start_time.setter
    def start_time(self, value):
        self.__start_time = self.check_time_format(value)

    @property
    def spent_time(self):
        running_time = time.mktime(time.localtime()) - self.start_time
        time_stamp = self.used_time + running_time
        return time_stamp

    @staticmethod
    def convert_timestamp(time_stamp):
        mins, secs = divmod(time_stamp, 60)
        hours, mins = divmod(mins, 60)
        format_time = "%02d:%02d:%02d" % (hours, mins, secs)
        return format_time

    def check_time_format(self, value):
        if isinstance(value, int):
            return value

        time_value = time.strptime(value, self._time_template)
        format_value = int(time.mktime(time_value))
        return format_value

    def show_time(self):
        self._current_times += 1
        spent_time = self.spent_time
        self.setText(self.convert_timestamp(spent_time))

    def start(self):
        self.on_start.emit()
        self._timer.start(1000)

    def stop(self):
        self._timer.stop()
        self.on_stop.emit()

        # 更新used_time
        self.used_time += self._current_times
        self._current_times = 0
