from PySide2 import QtWidgets, QtGui
from PySideLayoutTool.UIEditorLib.StringValidatorClass import checkString
from PySideLayoutTool.UIEditorLib import UIEditorScript

class BasicStringWidget(QtWidgets.QWidget):

    def __init__(self, default_text, validator=2, validators_lvl=0):
        super(BasicStringWidget, self).__init__()
        self.validator = self.validater_type(validator)
        self.validator_level = validators_lvl
        self.setMinimumHeight(40)
        self.setMaximumHeight(40)

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._str_widget = QtWidgets.QLineEdit()
        self._str_widget.setValidator(self.validator)
        self._str_widget.setText(default_text)

        self._layout.addWidget(self._str_widget)
        self.setLayout(self._layout)

        self._str_widget.textChanged.connect(self.updateText)

    def string_widget(self):
        return self._str_widget

    def updateText(self, arg__1):
        if self.validator == QtGui.QRegExpValidator and self.validator_level == 1:
            self._str_widget.setText(checkString(arg__1))

    def validater_type(self, index: int):
        return [
            QtGui.QIntValidator(),
            QtGui.QDoubleValidator(),
            QtGui.QRegExpValidator()
        ][index]


class MultiStringWidget(QtWidgets.QWidget):

    def __init__(self, use_color_text: bool):
        super(MultiStringWidget, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0,10,0,0)

        self._label_widget = QtWidgets.QLabel('None')

        self._multiline_text_widget = UIEditorScript.ScriptEditor() if use_color_text else QtWidgets.QPlainTextEdit()

        self._layout.addWidget(self._label_widget)
        self._layout.addSpacing(5)
        self._layout.addWidget(self._multiline_text_widget)

        self.setLayout(self._layout)

    def text_window_lines(self, min , max):
        pass


    def set_label_text(self, text: str):
        self._label_widget.setText(text)

    def text(self):
        return self._multiline_text_widget.document().toPlainText()