from PySide2 import QtWidgets, QtCore
from PySideLayoutTool.UIEditorTemplates.Common.LineEditTemplate import LineEditWidgets


class SliderWidget(QtWidgets.QWidget):
    def __init__(self):
        super(SliderWidget, self).__init__()
        self.setMaximumHeight(50)
        self.setMinimumHeight(50)

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self.slider = QtWidgets.QSlider()
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self._value = 0

        self._min = 0
        self._max = 1

        self._hor_layout = QtWidgets.QHBoxLayout()
        self._hor_layout.setContentsMargins(0, 0, 0, 0)
        self._hor_layout.setAlignment(QtCore.Qt.AlignLeft)

        self._hor_layout.addSpacing(5)
        self._hor_layout.addWidget(self.slider)

        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)

        self._layout.addLayout(self._hor_layout)
        self.setLayout(self._layout)

    def setRange(self,minValue,maxValue):
        self._min = minValue
        self._max = maxValue
        self.slider.setRange(minValue, maxValue)

    def clamp(self, num, min_value, max_value):
        return max(min(num,max_value),min_value)


class FloatSliderWidget(SliderWidget):

    def __init__(self):
        super(FloatSliderWidget, self).__init__()
        self.boxEdit = LineEditWidgets.LineEditFloatWidgetClass()
        self.boxEdit.setMinimumWidth(35)
        self.boxEdit.setMaximumWidth(35)

        self._hor_layout.insertWidget(0,self.boxEdit)

        self.slider.valueChanged.connect(self._set_slider_value)
        self.boxEdit._digital_widget.editingFinished.connect(self._set_box_value)
        self.boxEdit._digital_widget.valueChanged.connect(self._wheel_set_box_value)


    def setValue(self, value):
        self.boxEdit.setValue(value)
        self.slider.setValue(int(value * self._max))


    def _set_slider_value(self, value):
        if self._value != value:
            self._value = float(self.clamp(value, int(0  * 1000000.0), int(1 * 1000000.0)) / 1000000.0)
            self.boxEdit.setValue(round(self._value, 3))


    def _set_box_value(self):
        self._value = self.boxEdit.value()
        self.slider.setValue(int(1000000.0 * self._value))
        self.setFocus()


    def _wheel_set_box_value(self):
        if self.boxEdit.wheelState():
            self._value = self.boxEdit.value()
            self.slider.setValue(int(1000000.0 * self._value))





class IntSliderWidget(SliderWidget):
    def __init__(self):
        super(IntSliderWidget, self).__init__()
        self.boxEdit = LineEditWidgets.LineEditIntWidgetClass()
        self.boxEdit.setMaximumWidth(60)

        self._hor_layout.insertWidget(0, self.boxEdit)

        self.slider.valueChanged.connect(self._set_slider_value)
        self.boxEdit._digital_widget.editingFinished.connect(self._set_box_value)
        self.boxEdit._digital_widget.valueChanged.connect(self._wheel_set_box_value)


    def setValue(self, value):
        self.boxEdit.setValue(value)
        self.slider.setValue(int(value))


    def _set_slider_value(self, value):
        if self._value != value:
            self._value = value
            self.boxEdit.setValue(value)

    def _set_box_value(self):
        self._value = self.boxEdit.value()
        self.slider.setValue(self._value)
        self.setFocus()

    def _wheel_set_box_value(self):
        if self.boxEdit.wheelState():
            self._value = self._slider_widget.boxEdit.value()
            self.slider.setValue(self._value)