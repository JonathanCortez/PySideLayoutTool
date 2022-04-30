from PySide2 import QtWidgets

class RootWidget(QtWidgets.QWidget):
    """
        Root Widget when display on Layout UI Constructed view.
    """
    def __init__(self):
        super(RootWidget, self).__init__()
        self._text = QtWidgets.QTextEdit()
        self._text.setText('To make your custom UI layout,'
        ' just drag from Template Supported and drop on to Layout tree. '
        'If you need any help about certain inputs or how to make your own Template widget,'
        ' go to tab Help > Documentation.')


        self._layout = QtWidgets.QVBoxLayout()
        self._layout.addWidget(self._text)

        self.setLayout(self._layout)