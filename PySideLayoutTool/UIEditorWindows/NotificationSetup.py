from PySide2 import QtWidgets, QtCore, QtGui
import markdown

import importlib
from importlib import resources, util


class NotificationWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(NotificationWindow, self).__init__(parent)
        self.setWindowTitle('Notification Changes')

        size = QtCore.QSize(800, 500)
        self.setMinimumSize(size)

        self._layout = QtWidgets.QVBoxLayout()
        self._text_editor = QtWidgets.QTextEdit()
        self._text_editor.setReadOnly(True)
        self._text_editor.setProperty('class','markdown_display')

        self._text = None
        with importlib.resources.path("PySideLayoutTool.resources.data", "CHANGELOG.md") as path:
            with open(path, 'r') as file:
                self._text = markdown.markdown(file.read(), extensions=['extra'])

        self._text_editor.setHtml(self._text)
        self._layout.addWidget(self._text_editor)
        self.setLayout(self._layout)
