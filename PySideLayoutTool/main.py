import sys

from PySideLayoutTool.UIEditorLib import UISetupModule
from PySide2 import QtWidgets

import importlib.resources


def maya_main_window():
    import maya.OpenMayaUI as mayaUI
    import shiboken2
    main_window_ptr = mayaUI.MQtUtil_mainWindow()
    return shiboken2.wrapInstance(long(main_window_ptr), QtWidgets.QWidget)  # type: ignore


def houdini_main_window():
    import hou
    return hou.ui.mainQtWindow()


def DisplayWindow():
    with importlib.resources.path("resources.data", "UIEditorProject.uiproject") as path:
        UISetupModule.main_path(path)
        UISetupModule.PreInitialize(None, None)
        UISetupModule.Setup_Init()
    # path = __file__.replace('main.py', 'UIEditorProject.uiproject')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    with importlib.resources.open_text("resources.data", "LayoutToolBaseStyle.qss") as file:
        app.setStyleSheet(file.read())

    DisplayWindow()
    sys.exit(app.exec_())
