from PySideLayoutTool.UIEditorLib.UIEditorFactory import WidgetFactory
from PySideLayoutTool.UIEditorLib import LayoutTemplate, TemplateBuildClass
from PySide2 import QtWidgets
from . import CheckboxWidgetClass


class CheckClass(LayoutTemplate.ParmSetup):

    def __init__(self, parent):
        super(CheckClass, self).__init__(parent)
        self._checkbox = CheckboxWidgetClass.CheckBoxWidget()
        self._checkbox.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        self._state = 0

        self._layout.addWidget(self._checkbox)
        self._checkbox.stateChanged.connect(self.checkState)

    def checkState(self,state):
        self._state = state
        self.notify_expressions()

    def set_value(self, value):
        self._state = value
        self._checkbox.setChecked(bool(value))

    def eval(self):
        return self._checkbox.isChecked()


class CheckboxBuild(TemplateBuildClass.ParameterBuild):

    def widgetClass(self):
        return CheckClass


def register():
    WidgetFactory.register('Toggle', CheckboxBuild)