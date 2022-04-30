from PySide2 import QtWidgets, QtCore, QtGui
from PySideLayoutTool.UIEditorLib import UIEditorIconFactory, UIWindowManger


class FileWidgetLayout(QtWidgets.QWidget):

    def __init__(self):
        super(FileWidgetLayout, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0,0,0,0)

        self._hor_layout = QtWidgets.QHBoxLayout()
        self._hor_layout.setSpacing(0)
        self._hor_layout.setContentsMargins(0,2,0,2)
        self._hor_layout.setAlignment(QtCore.Qt.AlignLeft)


        self._geo_filter = ('*.abc *.ai *.bgeo *.bgeo.bz2 *.bgeo.gz *bgeo.lzma *.bgeo.sc *.bgeogz *.bgeosc *bhclassic *.bhclassic.bz2'
                            '*.bhclassic.gz *.bhclassic.lzma *.bhclassic.sc *.bhclassicgz *.bhclassicsc *.bjson *.bjson.gz *.bjson.sc *.bjsongz *.bjsonsc'
                            '*.bpoly *.bstl *.d *.dxf *.eps *.exr *.fbx *.flt *.geo *.geo.bz2 *.geo.gz *.geo.lzma *.geo.sc *.geogz *.geosc *.GoZ *.hclassic')
        self._image_filter = ('*.jpg *.png')

        self._file_dialog = QtWidgets.QFileDialog()
        self._text_box = QtWidgets.QLineEdit()

        self._button_widget = QtWidgets.QPushButton()
        self._button_widget.setMinimumWidth(30)
        self._button_widget.setMaximumWidth(30)
        # icon = QtGui.QIcon(UIEditorIconFactory.IconEditorFactory.create('add_file'))
        self._button_widget.setIcon(UIEditorIconFactory.IconEditorFactory.create('add_file'))

        self._hor_layout.addWidget(self._text_box)
        self._hor_layout.addSpacing(5)
        self._hor_layout.addWidget(self._button_widget)

        self._layout.addLayout(self._hor_layout)
        self.setLayout(self._layout)

        self._button_widget.pressed.connect(self.openFilePath)


    def set_text_value(self, path_str: str):
        self._text_box.setText(path_str)

    def file_widget_line(self):
        return self._text_box

    def openFilePath(self):
        file_name = self._file_dialog.getSaveFileName(self,'File Path', UIWindowManger.WindowsManger.root_save(), '*.')
        self._text_box.setText(file_name[0])

    def fileType(self, index: int):
        pass
