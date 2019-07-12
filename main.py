# coding:utf-8

import os
import sys

UI_PATH = os.path.join(os.path.dirname(__file__), 'ui')
LIBS_PATH = os.path.join(os.path.dirname(__file__), 'libs')
CORE_PATH = os.path.join(os.path.dirname(__file__), 'core')
UTILS_PATH = os.path.join(os.path.dirname(__file__), 'utils')

UI_PATH in sys.path or sys.path.append(UI_PATH)
LIBS_PATH in sys.path or sys.path.append(LIBS_PATH)
CORE_PATH in sys.path or sys.path.append(CORE_PATH)
UTILS_PATH in sys.path or sys.path.append(UTILS_PATH)

from MergeExcelWidget import main


if __name__ == '__main__':
    main()
