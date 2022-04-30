import sys

from UIEditorLib import UIModuleInterface
from PySide2 import QtWidgets


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
    # UIModuleInterface.Load_UI()
    # mainEditor = MainEditorWindow.EditorWindow('New_Test', 'NULL','User')
    # layoutWin = MainLayoutWindow.MainWindowLayout('New_Test')
    # UIEditorMediators.EditorsMediator(mainEditor,layoutWin)
    #
    # with open('E:/EpicGames/NewFeatures/Plugins/QuickUISetup/Json/Houdini/Python_UI_UE_Test.json') as file:
    #     LayoutConstructorClass.JsonConstructor.construct(file ,mainEditor)
    # mainEditor.show()



# app = None
# if not QtWidgets.QApplication.instance():
#     app = QtWidgets.QApplication(sys.argv)
# else:
#     app = QtWidgets.QApplication.instance()
#
# path = __file__.replace('main.py','UIEditorBaseStyle.css')
# with open(path) as file:
#     app.setStyleSheet(file.read())
# DisplayWindow()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    path = __file__.replace('main.py','UIEditorBaseStyle.css')
    with open(path) as file:
        app.setStyleSheet(file.read())
    DisplayWindow()
    sys.exit(app.exec_())