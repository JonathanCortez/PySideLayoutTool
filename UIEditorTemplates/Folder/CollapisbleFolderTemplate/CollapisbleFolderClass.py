from PySideLayoutTool.UIEditorLib import TemplateDataClass
from PySideLayoutTool.UIEditorLib.UIEditorProperty import UIProperty
from PySideLayoutTool.UIEditorLib.UIEditorFactory import WidgetFactory
from PySideLayoutTool.UIEditorLib.LayoutTemplate import FolderSetup
from PySideLayoutTool.UIEditorLib.TemplateBuildClass import FolderBuild
from . import CollapisbleFolderWidgetClass


class CollapisbleFolderClass(FolderSetup):

    def __init__(self,parent):
        super(CollapisbleFolderClass, self).__init__(parent)
        self._folder_widget = CollapisbleFolderWidgetClass.CollapsibleFolderWidget('None')

        self._layout.addWidget(self._folder_widget)


    @UIProperty(metaWidget='CheckProperty', label='Open on Start',category='Setting')
    def bOpen(self):
        pass

    def eval(self):
        return None

    def clearLayout(self):
        if self._folder_widget.collapisble_layout() is not None:
            for i in range(0, self._folder_widget.collapisble_layout().count()):
                item_layout = self._folder_widget.collapisble_layout().itemAt(i)
                widget = item_layout.widget()
                widget.deleteLater()

            for i in range(0, self._folder_layout.count()):
                item_layout = self._folder_layout.takeAt(i)
                self._folder_layout.removeItem(item_layout)
                del item_layout

        self._childWidgets = TemplateDataClass.TemplateGroup()
        self._folder_layout.addWidget(self._childWidgets)
        self._folder_widget.setTitle(self.label())
        self._folder_widget.setContentLayout(self._folder_layout)


    def PostUpdate(self):
        self._folder_widget.setContentLayout(self._folder_layout)


class CollapisbleFolderBuild(FolderBuild):

    def widgetClass(self):
        return CollapisbleFolderClass


def register():
    WidgetFactory.register('Collapsible', CollapisbleFolderBuild)