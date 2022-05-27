from PySideLayoutTool.UIEditorLib.UIEditorFactory import  WidgetFactory
from PySideLayoutTool.UIEditorLib import LayoutTemplate, TemplateBuildClass
from PySideLayoutTool.UIEditorLib.UIEditorProperty import UIProperty
from . import StringEditWidgetClass


class StringClass(LayoutTemplate.ParmSetup):

    def __init__(self,parent):
        super(StringClass, self).__init__(parent)
        self._textbox = None


    @UIProperty(metaWidget='CheckProperty', label='Multi-line String', category='Setting')
    def is_multi_line_string(self):
        pass

    @UIProperty(metaWidget='ComboProperty', label='Language', category='Setting', defaults=['None', 'Python'])
    def language_type(self):
        pass

    def bLabel(self) -> bool:
        return not self.is_multi_line_string()

    def PreUpdate(self):
        if self._textbox:
            self._textbox.deleteLater()

    def PostUpdate(self):
        if self.is_multi_line_string():
            self._textbox = StringEditWidgetClass.MultiStringWidget(bool(self.language_type().currentItem_index))
            self._textbox.set_label_text(self.label())
        else:
            self._textbox = StringEditWidgetClass.BasicStringWidget('')
            self._textbox.string_widget().editingFinished.connect(self._str_changed)

        self._layout.addWidget(self._textbox)


    def _str_changed(self):
        self.notify_expressions()

    def eval(self):
        if self.is_multi_line_string():
            return self._textbox.text()

        return self._textbox.string_widget().text()

    def set_value(self, value):
        if self.is_multi_line_string():
            self._textbox.insertPlainText(str(value))
        else:
            self._textbox.string_widget().setText(str(value))



class StringEditBuild(TemplateBuildClass.ParameterBuild):

    def widgetClass(self):
        return StringClass



def register():
    WidgetFactory.register('String', StringEditBuild)