from PySide2 import QtWidgets

class SeparatorHWidget(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(SeparatorHWidget, self).__init__(parent)
        self.setFixedHeight(20)
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._line = QtWidgets.QFrame()
        self._line.setFrameShape(QtWidgets.QFrame.HLine)
        self._line.setLineWidth(1)
        self._line.setStyleSheet("QFrame{"
                           "color: rgb(80, 80, 80);}")

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self._layout.addWidget(self._line)
        self.setLayout(self._layout)


class SeparatorVWidget(QtWidgets.QWidget):
    def __init__(self):
        super(SeparatorVWidget, self).__init__()
        self.setFixedWidth(20)
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._line = QtWidgets.QFrame()
        self._line.setFrameShape(QtWidgets.QFrame.VLine)
        self._line.setLineWidth(1)
        self._line.setStyleSheet("QFrame{"
                           "color: rgb(80, 80, 80);}")

        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self._layout.addWidget(self._line)
        self.setLayout(self._layout)