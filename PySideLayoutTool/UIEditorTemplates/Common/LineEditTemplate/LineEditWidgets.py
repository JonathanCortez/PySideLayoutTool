from PySide2 import QtWidgets, QtGui, QtCore

from abc import abstractmethod
from PySideLayoutTool.UIEditorTemplates.Common.SliderTemplate import SliderWidgetClass
from PySideLayoutTool.UIEditorTemplates.Common.LabelTemplate import LabelSwitchWidget


class LineEditWidgetClass(QtWidgets.QWidget):

    def __init__(self, parent):
        super(LineEditWidgetClass, self).__init__()
        self._parent = parent
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)

        self._hint_label = None

        self.setLayout(self._layout)

    def hint_text(self):
        return self._hint_label

    def addHint(self, text_str: str):
        pass

    def mousePressEvent(self, arg__1) -> None:
        if arg__1.button() == QtCore.Qt.MiddleButton:
            print('Middle')


class LineEditStrWidgetClass(LineEditWidgetClass):

    def __init__(self, parent, validater_index=0):
        super(LineEditStrWidgetClass, self).__init__(parent)
        self._str_widget = QtWidgets.QLineEdit()
        self._str_widget.setValidator(self.validater_type(validater_index))
        self._str_widget.setTextMargins(13, 0, 0, 0)

        self._layout.addWidget(self._str_widget)

    def changeText(self, text_str: str):
        self._str_widget.setText(text_str)

    def addHint(self, text_str: str):
        self._hint_label = text_str
        hint_label = QtWidgets.QLabel(self, text=text_str)
        hint_label.setAlignment(QtCore.Qt.AlignCenter)
        hint_label.setContentsMargins(0, 0, 0, 2)
        hint_label.setMinimumHeight(18)
        hint_label.setMaximumHeight(18)
        hint_label.setMinimumWidth(12)
        hint_label.setMaximumWidth(12)
        hint_label.setProperty('class', 'base_hint')
        return hint_label

    def validater_type(self, index: int):
        return [
            QtGui.QIntValidator(),
            QtGui.QDoubleValidator()
        ][index]


class LineEditDigitalWidgetClass(LineEditWidgetClass):

    def __init__(self, parent, min_value=0, max_value=1, steps=1, enable_switch_widget=False):
        super(LineEditDigitalWidgetClass, self).__init__(parent)
        self._hor_layout = QtWidgets.QHBoxLayout()
        self._hor_layout.setSpacing(0)
        self._hor_layout.setContentsMargins(0, 0, 0, 0)
        self._digital_widget = None
        self._enable_switch_widget = enable_switch_widget

        self._min = min_value
        self._max = max_value
        self._steps = steps

        self._bWheel = False

        self._layout.addLayout(self._hor_layout)

    def addHint(self, text_str: str):
        self._hint_label = text_str
        main_label_widget = None

        if self._enable_switch_widget:
            self._digital_widget.set_label_text(text_str)
            main_label_widget = self._digital_widget.label_widget()
        else:
            hint_label_widget = QtWidgets.QLabel(self, text=text_str)
            hint_label_widget.setAlignment(QtCore.Qt.AlignCenter)
            hint_label_widget.setContentsMargins(0, 0, 0, 2)
            hint_label_widget.setMinimumHeight(18)
            hint_label_widget.setMaximumHeight(18)
            hint_label_widget.setMinimumWidth(12)
            hint_label_widget.setMaximumWidth(12)
            hint_label_widget.setProperty('class', 'base_hint')
            self._digital_widget.setProperty('class', 'hint_property')
            main_label_widget = hint_label_widget

        self._hor_layout.insertWidget(0, main_label_widget)

        return main_label_widget

    def base_widget(self):
        return self._digital_widget.base_widget() if self._enable_switch_widget else self._digital_widget

    def wheelState(self):
        return self._bWheel

    def value(self):
        return self._digital_widget.base_widget().value() if self._enable_switch_widget else self._digital_widget.value()

    def setValue(self, value):
        self._digital_widget._main_widget.setValue(value) if self._enable_switch_widget else self._digital_widget.setValue(value)

    @abstractmethod
    def setRange(self, minValue, maxValue):
        self._min = minValue
        self._max = maxValue
        self._digital_widget._main_widget.setRange(minValue, maxValue) if self._enable_switch_widget else self._digital_widget.setRange(minValue, maxValue)


    def defaultMin(self):
        return self._min

    def defaultMax(self):
        return self._max

    def steps(self):
        return self._steps


class LineEditFloatWidgetClass(LineEditDigitalWidgetClass):

    def __init__(self, parent, minValue=0, maxValue=1, steps=0.1, no_num_button=True, enable_switch_widget=False):
        super(LineEditFloatWidgetClass, self).__init__(parent, minValue, maxValue, steps, enable_switch_widget)

        self._digital_widget = QtWidgets.QDoubleSpinBox()
        self._digital_widget.setSingleStep(self._steps)

        if no_num_button:
            self._digital_widget.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)

        if enable_switch_widget:
            self._digital_widget = LabelSwitchWidget.SwitchLabelWidget('None',SpinBoxWidget(minValue=minValue, maxValue=maxValue, steps=steps,  no_num_button=True))
            slider_widget = SliderWidgetClass.FloatSliderWidget()
            self._digital_widget.add_switch_widget(slider_widget)

            slider_widget.slider.valueChanged.connect(self.setValue)

        self._hor_layout.addWidget(self._digital_widget)
        self._digital_widget.installEventFilter(self)

    def setRange(self, minValue, maxValue):
        super(LineEditFloatWidgetClass, self).setRange(minValue,maxValue)
        if self._enable_switch_widget:
            self._digital_widget.child_widget().setRange(int(self._min * 1000000.0), int(self._max * 1000000.0))
            self._digital_widget.child_widget().boxEdit.setRange(float(self._min), float(self._max))

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Wheel:
            self._bWheel = True
        elif event.type() == QtCore.QEvent.Leave:
            self._bWheel = False
        else:
            self._bWheel = False

        return super(LineEditFloatWidgetClass, self).eventFilter(obj, event)

    @property
    def digital_widget(self):
        return self._digital_widget


class LineEditIntWidgetClass(LineEditDigitalWidgetClass):

    def __init__(self, parent, minValue=0, maxValue=1, steps=1, no_num_button=True, enable_switch_widget=False):
        super(LineEditIntWidgetClass, self).__init__(parent, minValue, maxValue, steps, enable_switch_widget)

        self._digital_widget = QtWidgets.QSpinBox()
        self._digital_widget.setSingleStep(self._steps)

        if no_num_button:
            self._digital_widget.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)

        if enable_switch_widget:
            self._digital_widget = LabelSwitchWidget.SwitchLabelWidget('None',SpinBoxWidget(minValue=minValue, maxValue=maxValue, steps=steps, no_num_button=no_num_button,integer_enable=True))
            slider_widget = SliderWidgetClass.IntSliderWidget()
            self._digital_widget.add_switch_widget(slider_widget)
            slider_widget.slider.valueChanged.connect(self.setValue)

        self._hor_layout.addWidget(self._digital_widget)
        self._digital_widget.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Wheel:
            self._bWheel = True
        elif event.type() == QtCore.QEvent.Leave:
            self._bWheel = False
        else:
            self._bWheel = False

        return super(LineEditIntWidgetClass, self).eventFilter(obj, event)


class SpinBoxWidget(QtWidgets.QWidget):

    def __init__(self, minValue=0, maxValue=1, steps=1, no_num_button=True, integer_enable=False):
        super(SpinBoxWidget, self).__init__()
        self.setMaximumHeight(50)
        self.setMinimumHeight(50)

        self._int_enable = integer_enable
        self._value = 0
        self._min = minValue
        self._max = maxValue

        self._digital_widget = QtWidgets.QSpinBox() if self._int_enable else QtWidgets.QDoubleSpinBox()
        self._digital_widget.setSingleStep(steps)

        if no_num_button:
            self._digital_widget.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)

        self._hor_layout = QtWidgets.QHBoxLayout()
        self._hor_layout.setContentsMargins(0, 0, 0, 0)
        self._hor_layout.addWidget(self._digital_widget)

        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)

        # self._layout.addLayout(self._hor_layout)
        self.setLayout(self._hor_layout)

    def clamp(self, num, min_value, max_value):
        return max(min(num,max_value),min_value)


    def base_widget(self):
        return self._digital_widget

    def setRange(self,min_value, max_value):
        if not self._int_enable:
            min_value = float(min_value)
            max_value = float(max_value)

        self._min = min_value
        self._max = max_value
        self._digital_widget.setRange(min_value, max_value)


    def setValue(self, value):
        self._value = value
        if not self._int_enable:
            self._value = float(self.clamp(value, int(self._min * 1000000.0), int(self._max * 1000000.0)) / 1000000.0)

        self._digital_widget.setValue(self._value)
