import importlib
from importlib import resources, util
import os, glob
from PySide2 import QtWidgets
import pickle

from PySideLayoutTool.UIEditorLib.UIEditorFactory import WidgetFactory
from PySideLayoutTool.UIEditorLib.UIWindowManger import WindowsManger
from PySideLayoutTool.UIEditorWindows import CreateUISetupWin
from typing import List
import json
import sys

main_given_path = ''
create_win_ptr = None


def main_path(path_str: str):
    global main_given_path
    main_given_path = path_str


def PreInitialize(func) -> None:
    if func:
        WindowsManger.setParentDCC(func)

    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()

    with importlib.resources.open_text("PySideLayoutTool.resources.data", "LayoutToolBaseStyle.qss") as file:
        app.setStyleSheet(file.read())

    package_path = importlib.util.find_spec('PySideLayoutTool.saved').submodule_search_locations[0]
    package_path = os.path.abspath(package_path)
    set_layout_file_save_root(package_path)

    with importlib.resources.path("PySideLayoutTool.resources.data", "UIEditorProject.uiproject") as path:
        with open(path) as file:
            data = json.load(file)
            load_modules(data['Modules'], False)
            load_modules(data['Plugins'], True)


def PostInitialize() -> None:
    path = WindowsManger.root_save()
    os.chdir(path)
    for file in glob.glob("*.qui"):
        full_path = path + f'/{file}'
        with open(full_path, 'rb') as uiFile:
            try:
                data = pickle.load(uiFile)
                WindowsManger.initilize_windows(data['Name'], full_path, data['Category'])
                WindowsManger.restoreState(data)
                uiFile.close()
            except:
                print(f'File : {uiFile} as failed.')


def set_layout_file_save_root(file_dir):
    WindowsManger.set_root_save(file_dir)


def Load_UI() -> None:
    file_dialog = QtWidgets.QFileDialog()
    full_file_path = file_dialog.getOpenFileName(None, 'Open File', WindowsManger.root_save(), '*.qui')
    with open(full_file_path[0], 'rb') as uiFile:
        data = pickle.load(uiFile)
        ui_name = data['Name']
        if WindowsManger.get_Stack(ui_name, 'User') is None:
            WindowsManger.initilize_windows(ui_name, full_file_path[0])
            WindowsManger.restoreState(data)
            WindowsManger.WindowShow(WindowsManger.get_Stack(ui_name, 'User')[ui_name + '_editor'])
        else:
            print(f'{ui_name} UI is is already loaded.')
        uiFile.close()


def Open_UI(main_name, win_type, category_name) -> None:
    win_dict = WindowsManger.get_Stack(main_name, category_name)
    win_instance = win_dict[win_type]
    WindowsManger.WindowShow(win_instance)


def Loaded_UIs() -> List[str]:
    return WindowsManger.window_names()


def Loaded_UI_Categories() -> List[str]:
    return WindowsManger.category_names()


def Loaded_UI_name_with_category(find_name, category_name):
    return WindowsManger.isNameInCategory(find_name, category_name)


def Setup_Init():
    global create_win_ptr
    create_win_ptr = CreateUISetupWin.UISetupWin()
    WindowsManger.WindowShow(create_win_ptr)


class ModuleInterface:
    """Represents a plugin interface. A plugin has a single register function."""

    def register(self) -> None:
        """Register the necessary widgets"""


def import_module(name: str) -> ModuleInterface:
    """Imports a module given a name."""
    return importlib.import_module(name)  # type: ignore


def load_modules(modules: List[str], bisPlugin) -> None:
    """Loads the plugins defined in the plugins list."""

    for module in modules:
        main_module = module['Name']

        if bisPlugin:
            if not bool(module['Enable']):
                continue

            main_module = "PySideLayoutTool.Plugins." + main_module
            uiplugin_path = module['Name']
            moduleLib = import_module(main_module)
            path = moduleLib.__file__.replace('__init__.py', f'{uiplugin_path}.uiplugin')


        else:
            base_module = main_module
            main_module = 'PySideLayoutTool.' + main_module
            moduleLib = import_module(main_module)
            path = moduleLib.__file__.replace('__init__.py', f'{base_module}.uiplugin')

        with open(path) as file:
            data = json.load(file)

            if "Bridge" in data:
                import_module(f'{main_module}.{data["Bridge"]}')

            if "Icons" in data:
                icon_module = import_module(f'{main_module}.{data["Icons"]}')
                icon_module.register()

            if 'Properties' in data:
                for property in data['Properties']:
                    import_module(f'{main_module}.{property}')

            if 'Categories' in data:
                for category in data['Categories']:
                    name = category['Name']
                    WidgetFactory.registerCategory(name)
                    for module in category['Modules']:
                        module = import_module(f'{main_module}.{name}.{module}')
                        module.register()
