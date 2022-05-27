from PySideLayoutTool.UIEditorLib import UIWindowManger
from PySide2 import QtCore, QtWidgets

class MainWindowLayout(QtWidgets.QMainWindow):
    def __init__(self, window_name: str):
        super(MainWindowLayout, self).__init__()
        self.setWindowTitle(f'{window_name} Layout')

        size = QtCore.QSize(450, 450)
        self.setMinimumSize(size)

        self._dock = QtWidgets.QDockWidget()
        self._dock.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self._layout_name = window_name
        self._serialization_obj = None

        self._widgets = {}

        self._widget_ptr = QtWidgets.QWidget()
        self._scrollArea = QtWidgets.QScrollArea()
        self._scrollArea.setWidgetResizable(True)
        self._scrollArea.setStyleSheet("QScrollArea{ border: 0px;}")

        self._dock.setWidget(self._scrollArea)

        self.addDockWidget(QtCore.Qt.TopDockWidgetArea,self._dock)


    def widget_layout(self):
        return self._widgets

    def closeEvent(self, event) -> None:
        self._serialization_obj.write_commonData()
        self._serialization_obj.saveData(force_save=True)

    def UpdateLayout(self, new_widget: QtWidgets.QWidget):
        self._widget_ptr.deleteLater()
        self._widget_ptr = new_widget
        self._scrollArea.setWidget(self._widget_ptr)
        self.update()

    def parm(self, name : str):
        return self._widgets[name]

    def templateLayout(self):
        return self._widget_ptr

    def layout_name(self):
        return self._layout_name

    def display(self):
        UIWindowManger.WindowsManger.WindowShow(self)

