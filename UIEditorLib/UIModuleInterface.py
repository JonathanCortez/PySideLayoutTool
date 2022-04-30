import importlib
import os, glob
from PySide2 import QtWidgets
import pickle

from PySideLayoutTool.UIEditorLib.UIEditorFactory import WidgetFactory
from PySideLayoutTool.UIEditorLib.UIWindowManger import WindowsManger
from PySideLayoutTool.UIEditorWindows import CreateUISetupWin
from typing import List
import json


main_given_path = ''
create_win_ptr = None

def main_path(path_str: str):
    global main_given_path
    main_given_path = path_str


def PreInitialize(func, base_save_path) -> None:
    if func:
        WindowsManger.setParentDCC(func)

    if base_save_path:
        WindowsManger.set_root_save(base_save_path)

    with open(main_given_path) as file:
        data = json.load(file)
        load_modules(data['Modules'], False)
        load_modules(data['Plugins'], True)


def PostInitialize() -> None:
    path = WindowsManger.root_save()
    os.chdir(path)
    for file in glob.glob("*.qui"):
        full_path = path + f'/{file}'
        with open(full_path, 'rb') as uiFile:
            data = pickle.load(uiFile)
            WindowsManger.InitilizeWindows(data['Name'], full_path, data['Category'])
            WindowsManger.restoreState(data)
            uiFile.close()


def set_UIFileBaseRoot(file_dir):
    WindowsManger.set_root_save(file_dir)


def Load_UI() -> None:
    file_dialog = QtWidgets.QFileDialog()
    full_file_path = file_dialog.getOpenFileName(None,'Open File',WindowsManger.root_save(),'*.qui')
    with open(full_file_path[0], 'rb') as uiFile:
        data = pickle.load(uiFile)
        ui_name = data['Name']
        if WindowsManger.get_Stack(ui_name,'User') is None:
            WindowsManger.InitilizeWindows(ui_name, full_file_path[0])
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
                return
            main_module = "Plugins." + main_module
            uiplugin_path = module['Name']
            moduleLib = import_module(main_module)
            path = moduleLib.__file__.replace('__init__.py', f'{uiplugin_path}.uiplugin')
        else:
            moduleLib = import_module(main_module)
            path = moduleLib.__file__.replace('__init__.py',f'{main_module}.uiplugin')

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
