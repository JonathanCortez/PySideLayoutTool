from PySide2 import QtWidgets
from PySideLayoutTool.UIEditorLib import LayoutTemplate, TemplateBuildClass, UIEditorFactory, TemplateDataClass


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

    def clearLayout(self):
        if self._folder_widget.layout() is not None:
            for i in range(0, self._folder_widget.layout().count()):
                item_layout = self._folder_widget.layout().itemAt(i)
                item_layout.widget().deleteLater()

        self._childWidgets = TemplateDataClass.TemplateGroup()
        self._folder_layout.addWidget(self._childWidgets)
        self._folder_widget.setLayout(self._folder_layout)

    def PostUpdate(self):
        self._folder_widget.setTitle(self.label())




class SimpleFolder(TemplateBuildClass.FolderBuild):

    def widgetClass(self):
        return SimpleFolderWidget



def register() -> None:
    UIEditorFactory.WidgetFactory.register('Simple', SimpleFolder)