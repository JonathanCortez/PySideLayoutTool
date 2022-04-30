from PySide2 import QtWidgets, QtGui, QtCore


class LineEditWidgetClass(QtWidgets.QWidget):

    def __init__(self):
        super(LineEditWidgetClass, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0,0,0,0)
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,QtWidgets.QSizePolicy.Fixed)

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

    def __init__(self, validater_index=0):
        super(LineEditStrWidgetClass, self).__init__()
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
        hint_label.setContentsMargins(0,0,0,2)
        hint_label.setMinimumHeight(18)
        hint_label.setMaximumHeight(18)
        hint_label.setMinimumWidth(12)
        hint_label.setMaximumWidth(12)
        hint_label.setProperty('class','base_hint')
        return hint_label

    def validater_type(self, index: int):
        return [
            QtGui.QIntValidator(),
            QtGui.QDoubleValidator()
        ][index]


class LineEditDigitalWidgetClass(LineEditWidgetClass):

    def __init__(self, min_value=0, max_value=1, steps=1):
        super(LineEditDigitalWidgetClass, self).__init__()
        self._hor_layout = QtWidgets.QHBoxLayout()
        self._hor_layout.setSpacing(0)
        self._hor_layout.setContentsMargins(0,0,0,0)
        self._digital_widget = None

        self._min = min_value
        self._max = max_value
        self._steps = steps

        self._bWheel = False

        self._layout.addLayout(self._hor_layout)

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
        self._digital_widget.setProperty('class','hint_property')
        self._hor_layout.insertWidget(0,hint_label)
        return hint_label


    def baseWidget(self):
        return self._digital_widget

    def wheelState(self):
        return self._bWheel

    def value(self):
        return self._digital_widget.value()

    def setValue(self, value):
        self._digital_widget.setValue(value)

    def setRange(self, minValue, maxValue):
        self._digital_widget.setRange(minValue, maxValue)

    def defaultMin(self):
        return self._min

    def defaultMax(self):
        return self._max

    def steps(self):
        return self._steps




class LineEditFloatWidgetClass(LineEditDigitalWidgetClass):

    def __init__(self, minValue=0,maxValue=1,steps=0.1):
        super(LineEditFloatWidgetClass, self).__init__(minValue, maxValue,steps)
        self._digital_widget = QtWidgets.QDoubleSpinBox()
        self._digital_widget.setSingleStep(self._steps)
        self._digital_widget.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)

        self._hor_layout.addWidget(self._digital_widget)
        self._digital_widget.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Wheel:
            self._bWheel = True
        elif event.type() == QtCore.QEvent.Leave:
            self._bWheel = False
        else:
            self._bWheel = False

        return super(LineEditFloatWidgetClass, self).eventFilter(obj, event)




class LineEditIntWidgetClass(LineEditDigitalWidgetClass):

    def __init__(self, minValue=0,maxValue=1,steps=1):
        super(LineEditIntWidgetClass, self).__init__(minValue, maxValue,steps)
        self._digital_widget = QtWidgets.QSpinBox()
        self._digital_widget.setSingleStep(self._steps)
        self._digital_widget.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)

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