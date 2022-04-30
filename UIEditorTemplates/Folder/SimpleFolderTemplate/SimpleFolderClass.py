from PySide2 import QtWidgets
from PySideLayoutTool.UIEditorLib import LayoutTemplate, TemplateBuildClass, UIEditorFactory


class SimpleFolderWidget(LayoutTemplate.FolderSetup):
    """ Simple Folder is good for keeping widgets together
        and with a label and frame around it.
    """
    def __init__(self,parent):
        super(SimpleFolderWidget, self).__init__(parent)
        self._folder_widget = QtWidgets.QGroupBox(title=self.label())
        self._folder_layout.addWidget(self._childWidgets)
        self._folder_widget.setLayout(self._folder_layout)

        self._layout.addWidget(self._folder_widget)

    def eval(self) -> int or float:
        return None

    # def callback(self) -> None:
    #     for observer in self._observingObjs:
    #         observer.evalCondition s()

    def clearLayout(self):
        super(SimpleFolderWidget, self).clearLayout()

    def PostUpdate(self):
        # super(SimpleFolderWidget, self).OnUpdate()
        # self._folder_layout.addWidget(self._childWidgets)
        self._folder_widget.setTitle(self.label())




class SimpleFolder(TemplateBuildClass.FolderBuild):

    def widgetClass(self):
        return SimpleFolderWidget



def register() -> None:
    UIEditorFactory.WidgetFactory.register('Simple', SimpleFolder)