from PySideLayoutTool.UIEditorLib import LayoutTemplate, TemplateBuildClass, UIEditorFactory
from . import FileWidgetClsss

class FileWidgetSetupClass(LayoutTemplate.ParmSetup):

    def __init__(self,parent):
        super(FileWidgetSetupClass, self).__init__(parent)
        self._file_widget = FileWidgetClsss.FileWidgetLayout()
        self._file_value = ''

        self._layout.addWidget(self._file_widget)
        self._file_widget.file_widget_line().editingFinished.connect(self._file_change)

    def _file_change(self):
        self._file_value = self._file_widget.file_widget_line().text()
        self.notify_expressions()

    def PostUpdate(self):
        pass

    def eval(self):
        return self._file_value

    def set_value(self, value):
        self._file_value = value
        self._file_widget.set_text_value(value)



class FileWidgetBuildClass(TemplateBuildClass.ParameterBuild):

    def widgetClass(self):
        return FileWidgetSetupClass


def register():
    UIEditorFactory.WidgetFactory.register('File', FileWidgetBuildClass)