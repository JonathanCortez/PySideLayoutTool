from PySideLayoutTool.UIEditorLib.UIEditorFactory import  WidgetFactory
from PySideLayoutTool.UIEditorLib import LayoutTemplate, TemplateBuildClass
from . import StringEditWidgetClass


class StringClass(LayoutTemplate.ParmSetup):

    def __init__(self,parent):
        super(StringClass, self).__init__(parent)
        self._textbox = StringEditWidgetClass.StringWidget(self.default_value())
        self._layout.addWidget(self._textbox)

        self._textbox.string_widget().editingFinished.connect(self._str_changed)

    def _str_changed(self):
        self.notify_expressions()

    def eval(self):
        return self._textbox.string_widget().text()

    def set_value(self, value):
        self._textbox.string_widget().setText(str(value))



class StringEditBuild(TemplateBuildClass.ParameterBuild):

    def widgetClass(self):
        return StringClass



def register():
    WidgetFactory.register('String', StringEditBuild)