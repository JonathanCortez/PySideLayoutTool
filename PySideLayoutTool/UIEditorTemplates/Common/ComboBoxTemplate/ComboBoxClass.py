from . import ComboBoxWidgetClass
from PySideLayoutTool.UIEditorLib.UIEditorProperty import UIProperty
from PySideLayoutTool.UIEditorLib import LayoutTemplate, TemplateBuildClass, UIEditorFactory

class ComboBoxSetupClass(LayoutTemplate.ParmSetup):

    def __init__(self, parent):
        super(ComboBoxSetupClass, self).__init__(parent)
        self._combo_widget = ComboBoxWidgetClass.ComboBoxWidget()
        self._current_index = 0

        self._layout.addWidget(self._combo_widget)
        self._combo_widget.combo_widget().activated.connect(self._combo_changed)

    @UIProperty(metaWidget='CheckProperty',label='Use Value as return value ',category='Combo Items', use_separator=True)
    def bItemValue(self):
        pass

    @UIProperty(metaWidget='DictionaryProperty',label='Values',category='Combo/Menu Items')
    def dict_keyValue(self):
        pass

    def _combo_changed(self, arg__1):
        self._current_index = arg__1
        self.notify_expressions()

    def eval(self):
        return self._current_index

    def set_value(self, value):
        self._combo_widget.setItem(int(value))

    def PostUpdate(self):
        items = self.dict_keyValue().keys
        self._combo_widget.addItems(items)


class ComboBoxBuildClass(TemplateBuildClass.ParameterBuild):

    def widgetClass(self):
        return ComboBoxSetupClass



def register():
    UIEditorFactory.WidgetFactory.register('Ordered Combo/Menu', ComboBoxBuildClass)


