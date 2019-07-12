# coding=utf8
# Copyright (c) 2018 CineUse
import Qt
from Qt import QtWidgets


def get_main_window(engine):
    main_window = None
    app = QtWidgets.QApplication.instance()
    if engine == "maya":
        import maya.OpenMayaUI as mui
        prt = mui.MQtUtil.mainWindow()
        if Qt.__binding__ == "PySide":
            import shiboken
            main_window = shiboken.wrapInstance(long(prt), QtWidgets.QWidget)
        if Qt.__binding__ == "PyQt4":
            import sip
            main_window = sip.wrapinstance(long(prt), QtWidgets.QWidget)
        elif Qt.__binding__ == "PySide2":
            import shiboken2
            main_window = shiboken2.wrapInstance(long(prt), QtWidgets.QWidget)
    elif engine == "nuke":
        for widgets in app.topLevelWidgets():
            if widgets.metaObject().className() == "Foundry::UI::DockMainWindow":
                main_window = widgets
                break
    elif engine == "max":
        import MaxPlus
        try:
            main_window = MaxPlus.GetQMaxMainWindow()
        except:
            main_window = MaxPlus.GetQMaxWindow()
    else:
        main_window = app.activeWindow()
    return main_window


if __name__ == "__main__":
    get_main_window()
