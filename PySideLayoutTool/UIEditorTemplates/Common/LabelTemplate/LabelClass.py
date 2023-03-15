from PySideLayoutTool.UIEditorLib import LayoutTemplate, TemplateBuildClass, UIEditorFactory
from PySide2 import QtWidgets,QtCore

class LabelSetupClass(LayoutTemplate.ParmSetup):

    def __init__(self,parent):
        super(LabelSetupClass, self).__init__(parent)
        self._label_widget = QtWidgets.QLabel(text='None')
        self._label_widget.setAlignment(QtCore.Qt.AlignLeft)
        self._layout.addWidget(self._label_widget)


    def PostUpdate(self):
        if self.default_value() != '':
            self._label_widget.setText(self.default_value())

    def eval(self):
        return self._label_widget.text()

    def set_value(self, value):
        self._label_widget.setText(str(value))



class LabelBuildClass(TemplateBuildClass.ParameterBuild):

    def widgetClass(self):
        return LabelSetupClass



def register():
    UIEditorFactory.WidgetFactory.register('Label', LabelBuildClass)
