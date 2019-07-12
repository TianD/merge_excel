# coding=utf8
from Qt import QtCompat


def setup_ui(uifile, base_instance=None):
    """Load a Qt Designer .ui file and returns an instance of the user interface
    Args:
        uifile (str): Absolute path to .ui file
        base_instance (QWidget): The widget into which UI widgets are loaded
        ui_class_info (dict): only used in PySide
    Returns:
        QWidget: the base instance
    """
    ui = QtCompat.load_ui(uifile)  # Qt.py mapped function
    if base_instance:
        for member in dir(ui):
            if not member.startswith('__') and \
               member is not 'staticMetaObject':
                setattr(base_instance, member, getattr(ui, member))


if __name__ == "__main__":
    pass
