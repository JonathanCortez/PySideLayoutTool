from PySide2 import QtWidgets,QtGui
from PySideLayoutTool.UIEditorLib.UIEditorIconFactory import IconEditorFactory

class ClampRangeWidget(QtWidgets.QWidget):

    def __init__(self, min, max, lockmin, lockmax, int_type=True, validator:bool=True):
        super(ClampRangeWidget, self).__init__()
        self._validator =  self.validator_type(validator)
        self._rangeLayout = QtWidgets.QHBoxLayout()
        self.setMinimumHeight(40)
        self.setMaximumHeight(40)
        self._icon_closed = QtGui.QIcon(IconEditorFactory.create('lock_closed'))
        self._icon_open = QtGui.QIcon(IconEditorFactory.create('lock_open'))

        self.minLock_widget = QtWidgets.QPushButton()
        self.minLock_widget.setFlat(True)
        self.minLock_widget.setIcon(QtGui.QIcon(IconEditorFactory.create('lock_open')))
        self.minLock_widget.setMinimumWidth(25)
        self.minLock_widget.setMaximumWidth(25)
        self.minLock_widget.setCheckable(True)
        self.minLock_widget.setChecked(lockmin)

        # Min Edit Line Setup
        self.minEdit_widget = QtWidgets.QSpinBox() if int_type else QtWidgets.QDoubleSpinBox()
        self.minEdit_widget.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.minEdit_widget.setValue(min)
        self.minEdit_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        # Max Edit Line Setup
        self.maxEdit_widget = QtWidgets.QSpinBox() if int_type else QtWidgets.QDoubleSpinBox()
        self.maxEdit_widget.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.maxEdit_widget.setValue(max)
        self.maxEdit_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.maxLock_widget = QtWidgets.QPushButton()
        self.maxLock_widget.setFlat(True)
        self.maxLock_widget.setIcon(QtGui.QIcon(IconEditorFactory.create('lock_open')))
        self.maxLock_widget.setMinimumWidth(25)
        self.maxLock_widget.setMaximumWidth(25)
        self.maxLock_widget.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.maxLock_widget.setCheckable(True)
        self.maxLock_widget.setChecked(lockmax)

        self._rangeLayout.addWidget(self.minLock_widget)
        self._rangeLayout.addWidget(self.minEdit_widget)
        self._rangeLayout.addWidget(self.maxEdit_widget)
        self._rangeLayout.addWidget(self.maxLock_widget)

        self.setLayout(self._rangeLayout)

        self.minLock_widget.pressed.connect(lambda: self.lockState(self.minLock_widget))
        self.maxLock_widget.pressed.connect(lambda: self.lockState(self.maxLock_widget))

    def lockState(self, button):
        if not button.isChecked():
            button.setIcon(self._icon_closed)
        else:
            button.setIcon(self._icon_open)

    def validator_type(self, type:bool):
        return QtGui.QIntValidator() if type else QtGui.QDoubleValidator()

    # def sizeHint(self) -> QtCore.QSize:
    #     return QtCore.QSize(30,30)