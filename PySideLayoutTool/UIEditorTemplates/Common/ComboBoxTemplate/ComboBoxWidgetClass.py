from PySide2 import QtWidgets, QtCore
from typing import List

class ComboBoxWidget(QtWidgets.QWidget):

    def __init__(self):
        super(ComboBoxWidget, self).__init__()
        self.setMinimumHeight(40)
        self.setMaximumHeight(40)
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)

        horizontal_Layout = QtWidgets.QHBoxLayout()
        horizontal_Layout.setSpacing(0)
        horizontal_Layout.setContentsMargins(0,0,0,0)

        self._combo_box = QtWidgets.QComboBox()
        self._combo_box.setEditable(False)
        self._combo_box.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self._combo_box.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLengthWithIcon)

        horizontal_Layout.addWidget(self._combo_box)
        # horizontal_Layout.addSpacerItem(QtWidgets.QSpacerItem(20,20,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Fixed))

        self._layout.addLayout(horizontal_Layout)
        self.setLayout(self._layout)

    def combo_widget(self):
        return self._combo_box

    def addItems(self, items: List[str]):
        self._combo_box.addItems(items)
        # TODO resize combo box to the longest string in items

    def addItem(self, item: str):
        self._combo_box.addItem(item)

    def setItem(self, index):
        self._combo_box.setCurrentIndex(index)