from PySide2 import QtWidgets, QtCore
from PySideLayoutTool.UIEditorLib import StringValidatorClass, UIWindowManger


class UISetupWin(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(UISetupWin, self).__init__(parent)
        self.setWindowTitle('UI Create')
        size = QtCore.QSize(450, 100)
        self.setMinimumSize(size)

        self._save_path = ''

        self._layout = QtWidgets.QVBoxLayout()
        self._form_layout = QtWidgets.QFormLayout()
        self._hor_layout = QtWidgets.QHBoxLayout()

        self._UI_name = QtWidgets.QLineEdit()
        self._path_str = QtWidgets.QLineEdit()
        self._category_str = QtWidgets.QLineEdit()
        self._category_str.setText('User')

        self._button_file_browser = QtWidgets.QPushButton()
        self._file_dialog = QtWidgets.QFileDialog()
        self._create_button = QtWidgets.QPushButton('Create')

        self._hor_layout.addWidget(self._path_str)
        self._hor_layout.addWidget(self._button_file_browser)

        self._form_layout.addRow('UI Name : ', self._UI_name)
        self._form_layout.addRow('UI Path : ', self._hor_layout)
        self._form_layout.addRow('Category : ', self._category_str)

        self._layout.addLayout(self._form_layout)
        self._layout.addWidget(self._create_button)

        self.setLayout(self._layout)

        self._UI_name.textChanged.connect(self.check_name)
        self._button_file_browser.pressed.connect(self.open_browser)
        self._create_button.pressed.connect(self.new_ui)

    def check_name(self):
        new_name = StringValidatorClass.checkString(self._UI_name.text())
        self._UI_name.setText(new_name)

    def open_browser(self):
        file_name = self._file_dialog.getSaveFileName(self,'Save Path', UIWindowManger.WindowsManger.root_save(), '.qui')
        self._save_path = file_name[0]
        self._path_str.setText(self._save_path)

    def new_ui(self):
        UIWindowManger.WindowsManger.InitilizeWindows(self._UI_name.text(), self._save_path, self._category_str.text())
        UIWindowManger.WindowsManger.WindowShow(
            UIWindowManger.WindowsManger.get_Stack(self._UI_name.text(), self._category_str.text())[self._UI_name.text() + '_editor'])
        self.close()



        