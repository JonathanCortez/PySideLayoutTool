import sys

from UIEditorLib import UIModuleInterface
from PySide2 import QtWidgets
from Resources import pysidetoolicons

def maya_main_window():
    import maya.OpenMayaUI as mayaUI
    import shiboken2
    main_window_ptr = mayaUI.MQtUtil_mainWindow()
    return shiboken2.wrapInstance(long(main_window_ptr), QtWidgets.QWidget) #type: ignore

def houdini_main_window():
    import hou
    return hou.ui.mainQtWindow()



def DisplayWindow():
    path = __file__.replace('main.py', 'UIEditorProject.uiproject')
    UIModuleInterface.main_path(path)
    UIModuleInterface.PreInitialize(None, None)
    UIModuleInterface.Setup_Init()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    path = __file__.replace('main.py','LayoutToolBaseStyle.qss')
    with open(path) as file:
        app.setStyleSheet(file.read())
    DisplayWindow()
    sys.exit(app.exec_())