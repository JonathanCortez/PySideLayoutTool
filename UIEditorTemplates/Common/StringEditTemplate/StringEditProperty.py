from PySideLayoutTool.UIEditorLib.UIEditorProperty import  UICProperty, PropertyFactory, IWidgetProperties
from . import StringEditWidgetClass

@PropertyFactory.register('LineEditProperty')
class StringProperty(IWidgetProperties):

    def __init__(self):
        super(StringProperty,self).__init__()
        self._strText: str = ''
        self._val_func = None
        self._verify_func = None

        self._textbox = StringEditWidgetClass.StringWidget(self._strText)
        self._layout.addWidget(self._textbox)

        self._textbox._str_widget.textChanged.connect(self.checkText)
        self._textbox._str_widget.editingFinished.connect(self.strUpdate)


    def override_default(self, defaults: tuple):
        self._textbox.validator = self._textbox.validater_type(defaults[0])
        self._textbox.validator_level = defaults[1]
        self._textbox._str_widget.setValidator(self._textbox.validator)
        self._textbox._str_widget.setText(defaults[2])
        self._val_func = defaults[3]

    def setText(self, new_text):
        self._textbox._str_widget.setText(new_text)

    def checkText(self, arg__1):
        if self._val_func is not None:
            self._textbox._str_widget.setText(self._val_func(arg__1))

        self._strText = self._textbox._str_widget.text()

    def strUpdate(self):
        self._strText = self._textbox._str_widget.text()
        self.setFocus()

    def setValue(self, value):
        self._textbox._str_widget.setText(value)

    def value(self):
        return self._textbox._str_widget.text()


    @UICProperty
    def strText(self):
        return self._strText

