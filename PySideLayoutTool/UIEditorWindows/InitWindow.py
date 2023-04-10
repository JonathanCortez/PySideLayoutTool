from PySide2 import QtWidgets, QtCore, QtGui
from PySideLayoutTool.UIEditorLib import StringValidatorClass, WindowsModule
from PySideLayoutTool.UIEditorTemplates.Common.SeparatorTemplate import SeparatorWidgetClass
from . import NotificationSetup


class UISetupWin(QtWidgets.QDialog):

    def __init__(self,notify_state: bool, settings_win, parent=None):
        super(UISetupWin, self).__init__(parent)
        self.setWindowTitle('Create Layout')
        size = QtCore.QSize(450, 150)
        self.setMinimumSize(size)
        self.setMaximumHeight(150)

        self._save_path = ''

        self._layout = QtWidgets.QVBoxLayout()
        self._form_layout = QtWidgets.QFormLayout()
        self._hor_layout = QtWidgets.QHBoxLayout()

        self._UI_name = QtWidgets.QLineEdit()
        self._path_str = QtWidgets.QLineEdit()
        self._category_str = QtWidgets.QLineEdit()
        self._category_str.setText('User')

        self._path_str.setText(WindowsModule.WindowsManger.root_save() + '/')
        self._notification_win = NotificationSetup.NotificationWindow()
        self._setting_win = settings_win

        self._button_file_browser = QtWidgets.QPushButton()
        self._file_dialog = QtWidgets.QFileDialog()
        self._create_button = QtWidgets.QPushButton('Create')

        self._setting_button = QtWidgets.QPushButton()
        self._setting_button.setFixedHeight(15)
        self._setting_button.setIcon(QtGui.QIcon(':/icons/setting_icon'))
        self._setting_button.setProperty('class', 'setting_button')
        self._setting_button.setToolTip(f"<p style='white-space:pre'> <B>Setting<B>")
        self._setting_button.setStyleSheet("QToolTip { color: #ffffff; background-color: #484848; border: 0px;}")

        self._hor_layout.addWidget(self._path_str)
        self._hor_layout.addWidget(self._button_file_browser)

        self._form_layout.addRow('UI Name : ', self._UI_name)
        self._form_layout.addRow('UI Path : ', self._hor_layout)
        self._form_layout.addRow('Category : ', self._category_str)

        self._layout.addLayout(self._form_layout)
        self._layout.addWidget(SeparatorWidgetClass.SeparatorHWidget())
        self._layout.addWidget(self._create_button)
        self._layout.addWidget(self._setting_button)

        self.setLayout(self._layout)

        if notify_state:
            WindowsModule.WindowsManger.window_show(self._notification_win)

        self._UI_name.textChanged.connect(self.check_name)
        self._button_file_browser.pressed.connect(self.open_browser)
        self._create_button.pressed.connect(self.new_ui)

        self._setting_button.pressed.connect(self._display_setting)

    def closeEvent(self, event):
        self._notification_win.close()
        self._setting_win.close()

    def event(self, event) -> bool:
        if event.type() == QtCore.QEvent.EnterWhatsThisMode:
            WindowsModule.WindowsManger.window_show(self._notification_win)

        return QtWidgets.QDialog.event(self, event)

    def _display_setting(self):
        WindowsModule.WindowsManger.window_show(self._setting_win)


    def check_name(self):
        new_name = StringValidatorClass.checkString(self._UI_name.text())
        self._UI_name.setText(new_name)
        full_name_path = WindowsModule.WindowsManger.root_save() + f'/{new_name}.qui'
        self._path_str.setText(full_name_path)
        self._save_path = full_name_path

    def open_browser(self):
        file_name = self._file_dialog.getSaveFileName(self, 'Save Path', WindowsModule.WindowsManger.root_save(),
                                                      '.qui')
        self._save_path = file_name[0]
        self._path_str.setText(self._save_path)

    def new_ui(self):
        if self._UI_name.text() == '':
            return

        WindowsModule.WindowsManger.initilize_windows(self._UI_name.text(), self._save_path, self._category_str.text())
        WindowsModule.WindowsManger.window_show(
            WindowsModule.WindowsManger.get_Stack(self._UI_name.text(), self._category_str.text())[
                self._UI_name.text() + '_editor'])
        self.close()
        self._notification_win.close()
        self._setting_win.close()
