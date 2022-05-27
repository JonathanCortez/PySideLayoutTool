from PySideLayoutTool.UIEditorLib.UIEditorProperty import  UICProperty, PropertyFactory, IWidgetProperties
from . import ClampRangeWidgetClass

@PropertyFactory.register('ClampProperty')
class ClampRangeProperty(IWidgetProperties):

    def __init__(self):
        super(ClampRangeProperty, self).__init__()
        self._min : int = 0
        self._max : int = 10
        self._lockmin : bool = False
        self._lockmax : bool = False

        self._clamp_widget = ClampRangeWidgetClass.ClampRangeWidget(self._min, self._max, self._lockmin, self._lockmax)
        self._layout.addWidget(self._clamp_widget)

        self._clamp_widget.minEdit_widget.valueChanged.connect(self.assignMin)
        self._clamp_widget.maxEdit_widget.valueChanged.connect(self.assignMax)
        self._clamp_widget.minLock_widget.pressed.connect(lambda: self.lockState(self._clamp_widget.minLock_widget))
        self._clamp_widget.maxLock_widget.pressed.connect(lambda: self.lockState(self._clamp_widget.maxLock_widget))


    def override_default(self, defaults: tuple):
        self._min = defaults[0]
        self._max = defaults[1] if len(defaults) == 2 else self._max
        self._lockmin = defaults[2] if len(defaults) == 3 else self._lockmin
        self._lockmax = defaults[3] if len(defaults) == 4 else self._lockmax
        self._clamp_widget.minEdit_widget.setValue(self._min)
        self._clamp_widget.maxEdit_widget.setValue(self._max)
        self._clamp_widget.minLock_widget.setChecked(self._lockmin)
        self._clamp_widget.maxLock_widget.setChecked(self._lockmax)

    def setValue(self, value):
        self._clamp_widget.minEdit_widget.setValue(value['minValue'])
        self._clamp_widget.maxEdit_widget.setValue(value['maxValue'])
        self._clamp_widget.minLock_widget.setChecked(value['minLock'])
        self._clamp_widget.maxLock_widget.setChecked(value['maxLock'])
        self._min = int(value['minValue'])
        self._max = int(value['maxValue'])
        self._lockmin = value['minLock']
        self._lockmax = value['maxLock']

    def value(self):
        clamp_dict = {}
        clamp_dict['minValue'] = self._clamp_widget.minEdit_widget.value()
        clamp_dict['maxValue'] = self._clamp_widget.maxEdit_widget.value()
        clamp_dict['minLock'] = self._clamp_widget.minLock_widget.isChecked()
        clamp_dict['maxLock'] = self._clamp_widget.maxLock_widget.isChecked()
        return clamp_dict

    def lockState(self, button):
        if button is self._clamp_widget.minLock_widget:
            self._lockmin = not button.isChecked()
        else:
            self._lockmax = not button.isChecked()


    def assignMin(self):
        self._min = int(self._clamp_widget.minEdit_widget.value())
        self.setFocus()


    def assignMax(self):
        self._max = int(self._clamp_widget.maxEdit_widget.value())
        self.setFocus()


    @UICProperty
    def min(self) -> int:
        """ min value for range"""
        return self._min

    @UICProperty
    def max(self) -> int:
        """ max value for range"""
        return self._max

    @UICProperty
    def minLock(self):
        return self._lockmin

    @UICProperty
    def maxLock(self):
        return self._lockmax