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
        self._folder_widget = FolderTabWidgetClass.FolderMultiTabWidget(self._childWidgets,parent=self)
        self._layout.addWidget(self._folder_widget)

        self._folder_widget.tabWidget.tabBarClicked.connect(self._new_tab_change)
        self._folder_widget.tabWidget.tabBar().tabCloseRequested.connect(self._close_tab_change)  # type: ignore

    @UIProperty(metaWidget='ComboProperty', label='Tab Placements', category='Setting', defaults=['Top','Left','Right'])
    def tabPlacement(self):
        pass


    def _new_tab_change(self,index ):
        if self._folder_widget.tabWidget.tabText(index) == "+":
            self.notify_expressions()

    def eval(self) -> int or float:
        return self._folder_widget.tabWidget.count()


    def clearLayout(self):
        count = self._folder_widget.count()
        if count >= 1:
            for i in range(0, count):
                widget_template = self._folder_widget.tabWidget.widget(i)
                widget_template.deleteLater()

            self._folder_widget.clear_tabwidget_data()

            for i in range(0,count):
                self._folder_widget.insert_tab(i)



    def PostUpdate(self):
        self._folder_widget.setPlacement(self.tabPlacement().currentItem_index)



class FolderMultiListWidgetClass(LayoutTemplate.FolderSetup):

    def __init__(self, scroll_enable=False, parent=None):
        super(FolderMultiListWidgetClass, self).__init__(parent)
        self._folder_widget = FolderTabWidgetClass.FolderMultiTabList(self._childWidgets,scroll_enable ,parent=self)
        self._layout.addWidget(self._folder_widget)

        self._folder_widget.add_button_widget().clicked.connect(self._new_widget)
        self._folder_widget.remove_button_widget().clicked.connect(self._close_tab_change)

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


class FolderMultiListScrollWidgetClass(FolderMultiListWidgetClass):

    def __init__(self, parent=None):
        super(FolderMultiListScrollWidgetClass, self).__init__(scroll_enable=True, parent=parent)




class FolderListTab(TemplateBuildClass.FolderBuild):

    def widgetClass(self):
        return FolderListClass



class MultiTabFolder(TemplateBuildClass.FolderBuild):

    def widgetClass(self):
        return FolderMultiTabClass


class MultiListWidgetFolder(TemplateBuildClass.FolderBuild):

    def widgetClass(self):
        return FolderMultiListWidgetClass


class MultiListScrollWidgetFolder(TemplateBuildClass.FolderBuild):

    def widgetClass(self):
        return FolderMultiListScrollWidgetClass


def register() -> None:
    UIEditorFactory.WidgetFactory.register('Tabs', FolderListTab)
    UIEditorFactory.WidgetFactory.register('Multiparm Block (Tabs)', MultiTabFolder)
    UIEditorFactory.WidgetFactory.register('Multiparm Block (List)', MultiListWidgetFolder)
    UIEditorFactory.WidgetFactory.register('Multiparm Block (Scroll)', MultiListScrollWidgetFolder)