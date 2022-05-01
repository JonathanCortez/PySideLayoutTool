from PySideLayoutTool.UIEditorLib import LayoutTemplate, TemplateBuildClass, UIEditorFactory, TemplateDataClass
from PySideLayoutTool.UIEditorLib.UIEditorProperty import UIProperty
from . import FolderTabWidgetClass

class FolderListClass(LayoutTemplate.FolderSetup):

    def __init__(self,parent=None):
        super(FolderListClass, self).__init__(parent)

    @UIProperty(metaWidget='CheckProperty', label='End Tab Group', category='Setting')
    def endGroup(self):
        pass

    def clearLayout(self):
        self._childWidgets.deleteLater()
        self._childWidgets = TemplateDataClass.TemplateGroup()

    def setParentTab(self, arg: bool):
        if arg:
            if self._folder_widget:
                self._folder_widget.deleteLater()

            self._folder_widget = FolderTabWidgetClass.FolderTabList(self, self._childWidgets)
            self._layout.addWidget(self._folder_widget)

    def bisFolderList(self):
        return True



class FolderMultiTabClass(LayoutTemplate.FolderSetup):

    def __init__(self,parent=None):
        super(FolderMultiTabClass, self).__init__(parent)
        self._folder_widget = FolderTabWidgetClass.FolderMultiTabWidget(self._childWidgets)
        self._layout.addWidget(self._folder_widget)

        self._folder_widget.tabWidget.tabBarClicked.connect(self._new_tab_change)
        self._folder_widget.tabWidget.tabBar().tabCloseRequested.connect(self._close_tab_change)  # type: ignore

    @UIProperty(metaWidget='ComboProperty', label='Tab Placements', category='Setting', defaults=['Top','Left','Right'])
    def tabPlacement(self):
        pass


    def _new_tab_change(self,index ):
        if self._folder_widget.tabWidget.tabText(index) == "+":
            self.notify_expressions()

    def _close_tab_change(self, index):
        self.notify_expressions()

    def eval(self) -> int or float:
        return self._folder_widget.tabWidget.count()


    def clearLayout(self):
        count = self._folder_widget.tabCount()
        if count >= 1:
            for i in range(count-1,-1,-1):
                widget = self._folder_widget.tabWidget.widget(i).layout().itemAt(0).widget()
                widget.deleteLater()

                if i != 0:
                    self._folder_widget.closeTab(i)

            self._childWidgets = TemplateDataClass.TemplateGroup()
            self._folder_widget.set_base_widget(self._childWidgets)
            self._folder_widget.tabContainer()[str(1)].addWidget(self._childWidgets)


    def PostUpdate(self):
        self._folder_widget.setPlacement(self.tabPlacement().currentItem_index)



class FolderMultiListWidgetClass(LayoutTemplate.FolderSetup):

    def __init__(self,parent=None):
        super(FolderMultiListWidgetClass, self).__init__(parent)
        self._folder_widget = FolderTabWidgetClass.FolderMultiTabList(self._childWidgets)
        self._layout.addWidget(self._folder_widget)

        self._folder_widget.add_button_widget().clicked.connect(self._new_widget)
        self._folder_widget.remove_button_widget().clicked.connect(self._new_widget)

    def _new_widget(self):
        self.notify_conditions()

    def eval(self) -> int or float:
        return self._folder_widget.count()

    def clearLayout(self):
        count = self._folder_widget.count()
        if count >= 1:
            self._folder_widget.clearWidgets()

            for i in range(0, count):
                self._folder_widget.new_widget()


    def PostUpdate(self):
        self._folder_widget.setName(self.label())





class FolderListTab(TemplateBuildClass.FolderBuild):

    def widgetClass(self):
        return FolderListClass



class MultiTabFolder(TemplateBuildClass.FolderBuild):

    def widgetClass(self):
        return FolderMultiTabClass


class MultiListWidgetFolder(TemplateBuildClass.FolderBuild):

    def widgetClass(self):
        return FolderMultiListWidgetClass


def register() -> None:
    UIEditorFactory.WidgetFactory.register('Tabs', FolderListTab)
    UIEditorFactory.WidgetFactory.register('Multiparm-TabFolder', MultiTabFolder)
    UIEditorFactory.WidgetFactory.register('Multiparm-ListFolder', MultiListWidgetFolder)