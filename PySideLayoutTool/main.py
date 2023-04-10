import sys

from PySideLayoutTool.UIEditorLib import SetupTools
from PySide2 import QtWidgets


def maya_main_window():
    import maya.OpenMayaUI as mayaUI
    import shiboken2
    main_window_ptr = mayaUI.MQtUtil_mainWindow()
    return shiboken2.wrapInstance(long(main_window_ptr), QtWidgets.QWidget)  # type: ignore


def houdini_main_window():
    import hou
    return hou.ui.mainQtWindow()


def DisplayWindow():
    # SetupTools.set_custom_plugin_loader(r'C:\Users\heata\PycharmProjects\PySideLayoutTool\PySideLayoutTool\Plugins')
    SetupTools.enable_notification(False)
    SetupTools.PreInitialize(None)
    SetupTools.Setup_Init()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    # with importlib.resources.open_text("resources.data", "LayoutToolBaseStyle.qss") as file:
    #     app.setStyleSheet(file.read())

    DisplayWindow()
    sys.exit(app.exec_())
