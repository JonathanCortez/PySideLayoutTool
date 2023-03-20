from PySide2 import QtWidgets, QtGui, QtCore


class SwitchLabelWidget(QtWidgets.QStackedWidget):

    def __init__(self, name: str, base_widget):
        super(SwitchLabelWidget, self).__init__()
        self._hint_label = name
        self._main_widget = base_widget

        self._switch_index = 0

        self._hint_label = LabelActionSwitch(name, self.switch_widgets)
        self._child_widget = None
        self.addWidget(self._main_widget)

    def add_switch_widget(self, widget):
        self._child_widget = widget
        self.addWidget(self._child_widget)
        self._main_widget.base_widget().valueChanged.connect(self._child_widget.set_slider_value)

    def switch_widgets(self):
        if self._switch_index == 0:
            self.setCurrentIndex(1)
            self._switch_index = 1
        else:
            self.setCurrentIndex(0)
            self._switch_index = 0

    def child_widget(self):
        return self._child_widget

    def base_widget(self):
        return self._main_widget

    def set_label_text(self, text: str):
        self._hint_label.setText(text)

    def label_widget(self):
        return self._hint_label


class LabelActionSwitch(QtWidgets.QLabel):

    def __init__(self, name: str, func):
        super(LabelActionSwitch, self).__init__()
        self._func = func

        self.setText(name)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setContentsMargins(0, 0, 0, 2)
        self.setMinimumHeight(18)
        self.setMaximumHeight(18)
        self.setMinimumWidth(12)
        self.setMaximumWidth(12)
        self.setProperty('class', 'base_hint')

    def mousePressEvent(self, event) -> None:
        self._func()
