from PySideLayoutTool.UIEditorLib import TemplateDataClass
from PySideLayoutTool.UIEditorLib.UIEditorProperty import UIProperty
from PySideLayoutTool.UIEditorLib.UIEditorFactory import WidgetFactory
from PySideLayoutTool.UIEditorLib.LayoutTemplate import FolderSetup
from PySideLayoutTool.UIEditorLib.TemplateBuildClass import FolderBuild
from . import CollapisbleFolderWidgetClass


class CollapisbleFolderClass(FolderSetup):

    def __init__(self,parent):
        super(CollapisbleFolderClass, self).__init__(parent)
        self._parent = parent
        self._folder_widget = CollapisbleFolderWidgetClass.CollapsibleFolderWidget(self._childWidgets)
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

        self._childWidgets = TemplateDataClass.TemplateGroup()
        self._folder_widget.new_frame(self._childWidgets)


    def PostUpdate(self):
        self._folder_widget.folder_title(self.label())
        # self._folder_widget.setContentLayout(self._folder_layout)
        # self._folder_widget.updateSize(0,10)
        # self._folder_widget.force_close()


class CollapisbleFolderBuild(FolderBuild):

    def widgetClass(self):
        return CollapisbleFolderClass




def register():
    WidgetFactory.register('Collapsible', CollapisbleFolderBuild)