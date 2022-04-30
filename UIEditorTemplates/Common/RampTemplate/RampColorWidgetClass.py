from PySide2 import QtWidgets, QtCore, QtGui
from . import RampWidgetClass


class RampColorWidgetSetup(QtWidgets.QWidget):

    def __init__(self, parent):
        super(RampColorWidgetSetup, self).__init__(parent)
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._parent = parent

        self.setFixedHeight(200)
        self._temp_label = QtWidgets.QLabel('Ramp Color not implemented yet.')

        self._layout.addWidget(self._temp_label,alignment=QtCore.Qt.AlignCenter)
        self.setLayout(self._layout)
