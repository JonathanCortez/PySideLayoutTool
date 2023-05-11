import importlib
from importlib import resources, util
import os, glob
from PySide2 import QtWidgets
import pickle

from PySideLayoutTool.resources import mypysidelayouticons_rc

from PySideLayoutTool.UIEditorLib.UIEditorFactory import WidgetFactory
from PySideLayoutTool.UIEditorLib.WindowsModule import WindowsManger
from PySideLayoutTool.UIEditorWindows import InitWindow, SettingWindow
from typing import List
import json
import sys

main_given_path = ''
create_win_ptr = None
custom_plugin_path = ''

tool_json_data = None
tool_json_path = None

notification_state = True

UNLOAD_MODULE = True
LOAD_MODULE = False

SETTING_WINDOW = None

def main_path(path_str: str):
    global main_given_path
    main_given_path = path_str


def set_custom_plugin_loader(plugin_path: str) -> None:
    if plugin_path not in sys.path:
        sys.path.append(plugin_path)

    global custom_plugin_path
    custom_plugin_path = plugin_path


def enable_notification(state: bool) -> None:
    global notification_state
    notification_state = state


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

    global tool_json_data, tool_json_path, SETTING_WINDOW

    with importlib.resources.path("PySideLayoutTool.resources.data", "PySideLayoutTool.uiproject") as path:
        tool_json_path = path
        with open(path) as file:
            data = json.load(file)
            tool_json_data = data
            __load_modules(data['Modules'], False)

    plugins_paths = []

    tool_plugin_path = importlib.util.find_spec('PySideLayoutTool.Plugins').submodule_search_locations[0]
    plugins_paths.append(tool_plugin_path)

    sys.path.append(tool_plugin_path)

    if custom_plugin_path:
        plugins_paths.append(custom_plugin_path)
        WindowsManger.set_plugin_path(custom_plugin_path)
    else:
        WindowsManger.set_plugin_path(tool_plugin_path)

    # Loading plugins
    for path in plugins_paths:
        folders = {}
        for dir in os.listdir(path):
            if os.path.isdir(os.path.join(path, dir)):
                if dir != '__pycache__':
                    folders[dir] = os.path.join(path, dir)

        plugin_names = [item['Name'] for item in tool_json_data['Plugins']]
        for name, full_path in folders.items():
            if f'{name}.uiplugin' in os.listdir(full_path):
                # Check if 'name' is in the list of plugin names
                if name in plugin_names:
                    index = plugin_names.index(name)
                else:
                    # If 'name' is not in the list, append it and update our list of plugin names
                    tool_json_data['Plugins'].append({'Name': name, 'Enable': False})
                    plugin_names.append(name)
                    # Get the index of the newly added plugin
                    index = len(plugin_names) - 1

                if tool_json_data['Plugins'][index]['Enable']:
                    load_plugin_modules(name, full_path, LOAD_MODULE)

                WindowsManger.add_plugin(name, tool_json_data['Plugins'][index]['Enable'], full_path)
            else:
                print(f'Plugin {name} is missing the .uiplugin file.')

        # for name, full_path in folders.items():
        #     index = [item['Name'] for item in tool_json_data['Plugins']].index(name)
        #     if f'{name}.uiplugin' in os.listdir(full_path):
        #         if len(tool_json_data['Plugins']) == 0:
        #             tool_json_data['Plugins'].append({'Name': name, 'Enable': False})
        #
        #         if name not in [item['Name'] for item in tool_json_data['Plugins']]:
        #             tool_json_data['Plugins'].append({'Name': name, 'Enable': False})
        #
        #         if tool_json_data['Plugins'][index]['Enable']:
        #             load_plugin_modules(name, full_path, LOAD_MODULE)
        #
        #         WindowsManger.add_plugin(name, tool_json_data['Plugins'][index]['Enable'], full_path)
        #
        #     else:
        #         print(f'Plugin {name} is missing the .uiplugin file.')

    with open(tool_json_path, 'w') as file:
        json.dump(tool_json_data, file, indent=4)

    SETTING_WINDOW = SettingWindow.SettingDisplay()


def tool_Json_data() -> tuple:
    global tool_json_data, tool_json_path
    return tool_json_data, tool_json_path


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
                print(f'File : {uiFile} has failed.')


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
            WindowsManger.window_show(WindowsManger.get_Stack(ui_name, 'User')[ui_name + '_editor'])
        else:
            print(f'{ui_name} UI is is already loaded.')
        uiFile.close()


def Open_UI(main_name, win_type, category_name) -> None:
    win_dict = WindowsManger.get_Stack(main_name, category_name)
    win_instance = win_dict[win_type]
    WindowsManger.window_show(win_instance)


def Loaded_UIs() -> List[str]:
    return WindowsManger.window_names()


def Loaded_UI_Categories() -> List[str]:
    return WindowsManger.category_names()


def Loaded_UI_name_with_category(find_name, category_name):
    return WindowsManger.isNameInCategory(find_name, category_name)


def Setup_Init():
    global create_win_ptr, SETTING_WINDOW
    create_win_ptr = InitWindow.UISetupWin(notification_state, SETTING_WINDOW)
    WindowsManger.window_show(create_win_ptr)


class ModuleInterface:
    """Represents a plugin interface. A plugin has a single register function."""

    def register(self) -> None:
        """Register the necessary widgets"""


def import_module(name: str) -> ModuleInterface:
    """Imports a module given a name."""
    return importlib.import_module(name)  # type: ignore


def __load_modules(modules: List[str], bisPlugin) -> None:
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

        __load_process(path, main_module)


def __load_process(path: str, module_path) -> None:
    with open(path) as file:
        data = json.load(file)

        if "Bridge" in data:
            import_module(f'{module_path}.{data["Bridge"]}')

        if "Icons" in data:
            if data["Icons"] != "":
                icon_module = import_module(f'{module_path}.{data["Icons"]}')
                icon_module.register()

        if 'Properties' in data:
            for property in data['Properties']:
                import_module(f'{module_path}.{property}')

        if 'Categories' in data:
            for category in data['Categories']:
                name = category['Name']
                WidgetFactory.registerCategory(name)
                for module in category['Modules']:
                    module = import_module(f'{module_path}.{name}.{module}')
                    module.register()


def __unload_process(path: str, module_path) -> None:
    with open(path) as file:
        data = json.load(file)

        if "Icons" in data:
            if data["Icons"] != "":
                icon_module = import_module(f'{module_path}.{data["Icons"]}')
                icon_module.unregister()

        if 'Categories' in data:
            for category in data['Categories']:
                name = category['Name']
                for module in category['Modules']:
                    module = import_module(f'{module_path}.{name}.{module}')
                    module.unregister()

def load_plugin_modules(plugin_name: str, path: str, load_type : bool) -> None:
    main_module = plugin_name
    uiplugin_path = path + f'\\{plugin_name}.uiplugin'
    import_module(main_module)

    if load_type:
        __unload_process(uiplugin_path, main_module)
    else:
        __load_process(uiplugin_path, main_module)

