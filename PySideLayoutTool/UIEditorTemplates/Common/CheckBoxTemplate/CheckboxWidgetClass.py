from PySide2 import QtWidgets, QtCore

class CheckBoxWidget(QtWidgets.QCheckBox):

    def __init__(self,checkstate=False):
        super(CheckBoxWidget, self).__init__()
        self.setMinimumHeight(30)
        self.setMaximumHeight(30)
        self.setChecked(checkstate)

