from PySide2 import QtWidgets, QtCore, QtGui
from typing import Dict

class CustomForm(QtWidgets.QVBoxLayout):

    def __init__(self):
        super(CustomForm, self).__init__()
        self.setSpacing(0)
        self.setContentsMargins(10 ,0 ,10 ,10)
        self.setAlignment(QtCore.Qt.AlignTop)

        self._label_widgets = {}

    def labels(self, widget):
        return self._label_widgets[widget]

    def new_Row(self, label :str,name:str, widget: QtWidgets.QWidget, spacing=15, apply_to_main=True):
        setup_layout = QtWidgets.QHBoxLayout()
        setup_layout.setContentsMargins(0 ,10 ,0 ,0)
        setup_layout.setSpacing(0)

        self._label_widget = QtWidgets.QLabel(text=label)
        self._label_widget.setMinimumHeight(30)
        self._label_widget.setMaximumHeight(30)

        if name is not None:
            self._label_widget.setToolTip(f"<p style='white-space:pre'> Parameter: <B>{name}<B></p>")
            self._label_widget.setStyleSheet("QToolTip { color: #ffffff; background-color: #484848; border: 0px;}")

        setup_layout.addWidget(self._label_widget ,alignment=QtCore.Qt.AlignLeft)
        setup_layout.addSpacing(spacing)
        setup_layout.addWidget(widget)

        if apply_to_main:
            self.addLayout(setup_layout)

        self._label_widgets[widget] = self._label_widget
        return setup_layout

    def add_Layout(self, layout_item):
        self.addLayout(layout_item)

    def add_Custom(self, widget: QtWidgets.QWidget):
        self.addWidget(widget)
