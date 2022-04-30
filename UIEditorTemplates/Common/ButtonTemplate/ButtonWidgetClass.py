from PySide2 import QtWidgets, QtCore, QtGui


class ButtonWidget(QtWidgets.QPushButton):

    def __init__(self, bState = False):
        super(ButtonWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred,QtWidgets.QSizePolicy.Fixed)
        self.setFlat(bState)
        self.setCheckable(bState)

    def changeText(self, text: str):
        self.setText(text)
        font = QtGui.QFont(text)
        font_metrics = QtGui.QFontMetrics(font)
        val = font_metrics.width(text)/4
        self.setMinimumWidth((24 - int(val)) + font_metrics.width(text))
        self.setMaximumWidth((24 - int(val)) + font_metrics.width(text))




class ButtonStripWidget(QtWidgets.QWidget):

    def __init__(self):
        super(ButtonStripWidget, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0,2,0,2)

        self._hor_layout = QtWidgets.QHBoxLayout()
        self._hor_layout.setSpacing(1)
        self._hor_layout.setContentsMargins(0,0,0,0)
        self._hor_layout.setAlignment(QtCore.Qt.AlignLeft)

        self._button_list = []
        self._last_selected = None
        self._last_button = None
        self._type = 0

        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)

        self._layout.addLayout(self._hor_layout)
        self.setLayout(self._layout)

    def addButton(self, text):
        button = ButtonWidget(True)
        button.changeText(text)
        self._hor_layout.addWidget(button)
        self._button_list.append(button)

        button.pressed.connect(lambda pass_obj=button: self.updateSelected(pass_obj))

        return button


    def addButtons(self,texts: list):
        count = len(texts)
        for i in enumerate(texts):
            new_button = self.addButton(i[1])
            if i[0] == 0:
                new_button.setProperty('class','first_button')
            elif i[0] == count-1:
                new_button.setProperty('class','last_button')


    def updateSelected(self, button_pressed):
        for i in enumerate(self._button_list):
            if i[1] == button_pressed:
                self._last_selected = i[0]
                self._last_button = i[1]
                break

        if self._type != 2:
            for i in enumerate(self._button_list):
                if i[0] != self._last_selected:
                    i[1].setChecked(False)

    def typeStrip(self, index: int):
        self._type = index

    def clearButtons(self):
        self._button_list.clear()
        self._last_button = None

    def lastSelected(self):
        return (self._last_selected, self._last_button)

    def checked_buttons(self):
        buttons_checked = []
        for i in enumerate(self._button_list):
            if i[1].isChecked():
                buttons_checked.append(i)

        return buttons_checked