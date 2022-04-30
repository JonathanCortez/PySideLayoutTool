from PySideLayoutTool.UIEditorLib.UIEditorProperty import  UICProperty, PropertyFactory, IWidgetProperties
from . import CheckboxWidgetClass

@PropertyFactory.register('CheckProperty')
class CheckProperty(IWidgetProperties):

    def __init__(self):
        super(CheckProperty, self).__init__()
        self._markState = False

        self._checkbox = CheckboxWidgetClass.CheckBoxWidget()
        self._layout.addWidget(self._checkbox)

        self._checkbox.stateChanged.connect(self.checkState)

    def override_default(self, defaults: tuple):
        self._markState = defaults[0]
        self._checkbox.setChecked(self._markState)

    def checkState(self, arg):
        self._markState = True if arg == 2 else False

    def setValue(self,value):
        self._checkbox.setChecked(value)

    def value(self):
        return self._checkbox.isChecked()


    @UICProperty
    def mark(self):
        return self._markState
