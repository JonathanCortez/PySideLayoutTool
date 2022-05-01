# import hou

from PySideLayoutTool.UIEditorLib import UIEditorMediators, UIWindowManger
from PySide2 import QtCore, QtWidgets

class MainWindowLayout(QtWidgets.QMainWindow, UIEditorMediators.BaseComponent):
    def __init__(self, window_name: str):
        super(MainWindowLayout, self).__init__()
        self.setWindowTitle(f'{window_name} Layout')

        size = QtCore.QSize(450, 450)
        self.setMinimumSize(size)

        self._dock = QtWidgets.QDockWidget()
        self._dock.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self._ID_name = ''

        self._widget_ptr = QtWidgets.QWidget()
        self._scrollArea = QtWidgets.QScrollArea()
        self._scrollArea.setWidgetResizable(True)
        self._scrollArea.setStyleSheet("QScrollArea{ border: 0px;}")

        self._dock.setWidget(self._scrollArea)

        self.addDockWidget(QtCore.Qt.TopDockWidgetArea,self._dock)


    def closeEvent(self, event) -> None:
        self.mediator.notify_force_update() #type: ignore

    def UpdateLayout(self, new_widget: QtWidgets.QWidget):
        self._widget_ptr = new_widget
        self._scrollArea.setWidget(self._widget_ptr)
        self.update()

    def parm(self, name : str):
        return self._widget_ptr.find_widget(name)

    def templateLayout(self):
        return self._widget_ptr

    def layout_name(self):
        return self._ID_name

    def display(self):
        UIWindowManger.WindowsManger.WindowShow(self)

