from . import DictionaryWidgetClass
from PySideLayoutTool.UIEditorLib import LayoutTemplate, TemplateBuildClass, UIEditorFactory


class DictionarySetupClass(LayoutTemplate.ParmSetup):

    def __init__(self, parent):
        super(DictionarySetupClass, self).__init__(parent)
        self._dict_widget = DictionaryWidgetClass.DictWidgetClass()
        self._row_change = 0
        self._column_change = 0

        self._layout.addWidget(self._dict_widget)
        self._dict_widget.table_widget.cellChanged.connect(self._dict_changed)


    def _dict_changed(self,row, column):
        self._row_change = row
        self._column_change = column
        self.notify_expressions()


    def eval(self):
        return self._row_change, self._column_change

    def PostUpdate(self):
        pass



class DictionaryBuildClass(TemplateBuildClass.ParameterBuild):

    def widgetClass(self):
        return DictionarySetupClass


def register():
    UIEditorFactory.WidgetFactory.register('Key-Value Dictionary', DictionaryBuildClass)



