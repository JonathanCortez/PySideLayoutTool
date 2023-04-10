import importlib
from importlib import resources
from typing import Dict
import re

from PySide2 import QtWidgets, QtCore, QtGui
from PySideLayoutTool.UIEditorLib import SetupTools, WindowsModule, StringValidatorClass
from PySideLayoutTool.UIEditorTemplates.Folder.CollapisbleFolderTemplate import CollapisbleFolderWidgetClass
from PySideLayoutTool.UIEditorTemplates.Common.SeparatorTemplate import SeparatorWidgetClass
from PySideLayoutTool.UIEditorTemplates.Folder.TabFolderTemplate.FolderTabWidgetClass import FolderMultiTabList

import json
import os

class SettingDisplay(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(SettingDisplay,self).__init__(parent)
        self.setWindowTitle('Settings')
        self._size = QtCore.QSize(500, 700)
        self.setMinimumSize(self._size)

        self._layout = QtWidgets.QVBoxLayout()
        self._splitter = QtWidgets.QSplitter()
        self._splitter.setChildrenCollapsible(False)
        self._splitter.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self._splitter.setProperty('splitter_settings', 1)

        self._opt_widget = OptionsDisplay(self)
        self._plugin_display = PluginDisplay()

        self._splitter.addWidget(self._opt_widget)
        self._splitter.addWidget(self._plugin_display)

        self._layout.addWidget(self._splitter)

        self.setLayout(self._layout)

    def closeEvent(self, event):
        if self._plugin_display._plugin_create_win is not None:
            self._plugin_display._plugin_create_win.close()


class OptionsDisplay(QtWidgets.QWidget):

    def __init__(self,parent):
        super(OptionsDisplay, self).__init__(parent)
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setAlignment(QtCore.Qt.AlignTop)
        self._parent = parent

        self._plugin_button = QtWidgets.QPushButton('Plugins')
        self._layout.addWidget(self._plugin_button)


        self.setLayout(self._layout)

        self._plugin_button.pressed.connect(self.change_display)

    def change_display(self):
        pass



class PluginDisplay(QtWidgets.QWidget):

    def __init__(self):
        super(PluginDisplay, self).__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setAlignment(QtCore.Qt.AlignTop)

        self._scroll_area = QtWidgets.QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setStyleSheet("QScrollArea{ border: 0px; background-color: #1f1f1f; border-radius: 8px; }")
        self._scroll_area.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self._plugins_found_list = Plugins_Layout_Display(self)
        self._create_plugin_button = QtWidgets.QPushButton('New Plugin')
        self._plugin_create_win = None

        self._scroll_area.setWidget(self._plugins_found_list)

        self._layout.addWidget(self._scroll_area)
        self._layout.addWidget(SeparatorWidgetClass.SeparatorHWidget())
        self._layout.addWidget(self._create_plugin_button)

        self.setLayout(self._layout)


        self._create_plugin_button.pressed.connect(self.create_plugin)

    def plugin_create_win(self):
        return self._plugin_create_win

    def create_plugin(self):
        if self._plugin_create_win is None:
            self._plugin_create_win = Plugin_Create(self._plugins_found_list)
            WindowsModule.WindowsManger.window_show(self._plugin_create_win)
        else:
            self._plugin_create_win.setFocus()



class Plugins_Layout_Display(QtWidgets.QWidget):

    def __init__(self, parent):
        super(Plugins_Layout_Display, self).__init__(parent)
        self._parent = parent

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setAlignment(QtCore.Qt.AlignTop)

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self._plugins_displayed = []
        self.update_plugin_list()

        self.setLayout(self._layout)


    def update_plugin_list(self):
        for name in WindowsModule.WindowsManger.get_plugins():
            if name not in self._plugins_displayed:
                folder_layout = QtWidgets.QFormLayout()
                checkbox = QtWidgets.QCheckBox()
                checkbox.setChecked(not WindowsModule.WindowsManger.get_plugins()[name]['Enabled'])
                checkbox.checkState()

                path = WindowsModule.WindowsManger.get_plugins()[name]['Path']

                setattr(checkbox, 'plugin_name', name)
                setattr(checkbox, 'plugin_enabled', WindowsModule.WindowsManger.get_plugins()[name]['Enabled'])
                setattr(checkbox, 'plugin_path', path)

                text_label = QtWidgets.QLabel()
                text_label.setProperty('class', 'markdown_display')
                text_label.setFixedHeight(20)
                text_label.setText(path)

                folder_layout.addRow('Enabled : ', checkbox)
                folder_layout.addRow('Path : ', text_label)

                folder = CollapisbleFolderWidgetClass.CollapsibleFolderWidgetV2(name)
                folder.setContentLayout(folder_layout, speed=450)
                folder.updateSize(folder_layout.sizeHint().width(), 5)
                folder.force_close()

                self._plugins_displayed.append(name)

                self._layout.addWidget(folder)

                checkbox.stateChanged.connect(self.plugin_enabled)

    def plugin_enabled(self, state):
        index = 0
        data = SetupTools.tool_Json_data()[0]
        path = SetupTools.tool_Json_data()[1]
        for inner_index, plugin in enumerate(data['Plugins']):
            if plugin['Name'] == self.sender().__dict__['plugin_name']:
                index = inner_index
                break

        if not self.sender().isChecked():
            SetupTools.load_plugin_modules(self.sender().__dict__['plugin_name'], self.sender().__dict__['plugin_path'],
                                           SetupTools.LOAD_MODULE)
            data['Plugins'][index]['Enable'] = True

            with open(path, 'w') as file:
                json.dump(data, file, indent=4)

        else:
            SetupTools.load_plugin_modules(self.sender().__dict__['plugin_name'], self.sender().__dict__['plugin_path'],
                                           SetupTools.UNLOAD_MODULE)
            data['Plugins'][index]['Enable'] = False

            with open(path, 'w') as file:
                json.dump(data, file, indent=4)



class Plugin_Create(QtWidgets.QDialog):

    def __init__(self, parent):
        super(Plugin_Create, self).__init__()
        self.setWindowTitle('Create Plugin')
        self.setMinimumSize(700, 200)
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)

        self._parent = parent

        self._layout = QtWidgets.QFormLayout()
        self._layout.setAlignment(QtCore.Qt.AlignTop)

        self._base_path = WindowsModule.WindowsManger.get_plugin_path()

        self._plugin_name = QtWidgets.QLineEdit()

        self._path = QtWidgets.QLineEdit()
        self._path.setText(self._base_path)

        self._tab_widget = plugin_tab_widget(self)
        self._tab_widget_data = {}

        self._tablist_widget = FolderMultiTabList(self._tab_widget, True)
        self._tablist_widget.new_widget()
        self._tablist_widget.set_minimum_count(1)

        self._enable_icon = QtWidgets.QCheckBox()
        self._enable_icon.setChecked(True)

        self._create_button = QtWidgets.QPushButton('Create')

        self._layout.addRow('Plugin Name : ', self._plugin_name)
        self._layout.addRow('Path : ', self._path)

        self._layout.addWidget(SeparatorWidgetClass.SeparatorHWidget())
        self._layout.addWidget(self._tablist_widget)

        self._layout.addWidget(SeparatorWidgetClass.SeparatorHWidget())
        self._layout.addRow('Enable Icon : ', self._enable_icon)
        self._layout.addWidget(SeparatorWidgetClass.SeparatorHWidget())

        self._layout.addWidget(self._create_button)

        self.setLayout(self._layout)

        self._create_button.pressed.connect(self.create_plugin)
        self._plugin_name.textChanged.connect(self.check_plugin_name)

    def closeEvent(self, event):
        self._parent._parent._plugin_create_win = None

    def check_plugin_name(self):
        new_name = StringValidatorClass.checkString(self._plugin_name.text())
        self._plugin_name.setText(new_name)

    def update_date(self, widget):
        self._tab_widget_data[f'{self._tablist_widget.count()}'] = widget

    def create_plugin(self):
        for index, widget in self._tab_widget_data.items():
            if widget.get_name() == '':
                widget.get_name_widget().setFocus()
                return

            if widget.get_category() == '' and widget.get_category_widget().isEnabled():
                widget.get_category_widget().setFocus()
                return

        plugin_dir = os.path.join(self._base_path, self._plugin_name.text())
        os.makedirs(plugin_dir, exist_ok=True)

        with open(os.path.join(plugin_dir, '__init__.py'), 'w') as f:
            pass

        plugin_sub_categories = {}
        plugin_sub_dirs = {}
        plugin_sub_template_dir = {}
        plugin_category_count = {}

        properties = []

        for index, widget in self._tab_widget_data.items():
            if widget.get_category() not in plugin_category_count:
                plugin_category_count[widget.get_category()] = 1
            else:
                plugin_category_count[widget.get_category()] += 1

        for index, widget in self._tab_widget_data.items():
            name = widget.get_name()
            category = widget.get_category()
            extension_type = widget.get_type()
            spaced_name = name.replace('_', ' ')

            if extension_type == 'Property':
                plugin_property_dir = os.path.join(plugin_dir, 'Properties')
                os.makedirs(plugin_property_dir, exist_ok=True)

                if not os.path.isfile(os.path.join(plugin_property_dir, '__init__.py')):
                    with open(os.path.join(plugin_property_dir, '__init__.py'), 'w') as f:
                        pass

                properties.append(f'Properties.{name}Property')
                plugin_sub_template_dir[f'{name}'] = {'path' : plugin_property_dir}
                plugin_sub_categories['None'] = []
                plugin_sub_categories['None'].append({'Name': name, 'Space_name': spaced_name, 'Type': extension_type, 'Module_Path': f'Properties.{name}'})

            else:
                if category not in plugin_sub_categories:
                    plugin_sub_categories[f'{category}'] = []

                    plugin_category_dir = os.path.join(plugin_dir, category)
                    os.makedirs(plugin_category_dir, exist_ok=True)

                    plugin_sub_dirs[f'{category}'] = plugin_category_dir

                    with open(os.path.join(plugin_category_dir, '__init__.py'), 'w') as f:
                        pass

                    if plugin_category_count[category] > 1:
                        plugin_widget_template_dir = os.path.join(plugin_category_dir, f'{name}Template')
                        os.makedirs(plugin_widget_template_dir, exist_ok=True)

                        with open(os.path.join(plugin_widget_template_dir, '__init__.py'), 'w') as f:
                            pass

                        plugin_sub_categories[f'{category}'].append({'Name': name,'Space_name': spaced_name, 'Type' : extension_type, 'Module_Path': f'{name}Template.{name}Setup'})
                        plugin_sub_template_dir[f'{name}'] = {'category' : category, 'path' : plugin_widget_template_dir}

                    else:
                        plugin_sub_categories[f'{category}'].append({'Name': name,'Space_name': spaced_name, 'Type' : extension_type, 'Module_Path': f'{name}Setup'})
                        plugin_sub_template_dir[f'{name}'] = {'category': category, 'path': plugin_category_dir}

                else:
                    plugin_category_dir = plugin_sub_dirs[f'{category}']

                    if plugin_category_count[category] > 1:
                        plugin_widget_template_dir = os.path.join(plugin_category_dir, f'{name}Template')
                        os.makedirs(plugin_widget_template_dir, exist_ok=True)

                        with open(os.path.join(plugin_widget_template_dir, '__init__.py'), 'w') as f:
                            pass

                        plugin_sub_categories[f'{category}'].append({'Name': name,'Space_name': spaced_name, 'Type' : extension_type, 'Module_Path': f'{name}Template.{name}Setup'})
                        plugin_sub_template_dir[f'{name}'] = {'category': category, 'path': plugin_widget_template_dir}
                    else:
                        plugin_sub_categories[f'{category}'].append({'Name': name,'Space_name': spaced_name, 'Type' : extension_type, 'Module_Path': f'{name}Setup'})
                        plugin_sub_template_dir[f'{name}'] = {'category': category, 'path': plugin_category_dir}


        with importlib.resources.open_text("PySideLayoutTool.UIEditorLib", "boilerplate_class.py") as f:
            # Read the contents of the file into a string
            boilerplate_file = f.read()
            sections = boilerplate_file.split("#------------------------------")

            for category in plugin_sub_categories:
                for item in plugin_sub_categories[category]:
                    name = item['Name']
                    extension_type = item['Type']
                    spaced_name = item['Space_name']

                    new_string_sections = []
                    new_string_sections.extend(sections)
                    widget_setup_file = new_string_sections[0]

                    # Add a new line at index 5
                    new_line = f'from . import {name}Layout\n'
                    lines = widget_setup_file.splitlines()
                    lines.insert(5, new_line)
                    widget_setup_file = '\n'.join(lines)

                    new_string_sections.pop(0)
                    new_string_sections.insert(0, widget_setup_file)

                    for index, string_section in enumerate(new_string_sections):
                        # Replace all occurrences of 'WIDGETNAME' and 'LABELWIDGETNAME' in the modified string
                        replacements = {
                            r'NAME': f'{name}',
                            r'\bWIDGET LABEL\b': f'{spaced_name}',
                            r'\bSETUPTYPE\b': f'{"ParmSetup" if extension_type == "Parameter" else "FolderSetup"}',
                            r'\bBUILDTYPE\b': f'{"ParameterBuild" if extension_type == "Parameter" else "FolderBuild"}',
                        }
                        for pattern, replacement in replacements.items():
                            string_section = re.sub(pattern, replacement, string_section)

                        if '#------------------------------' in string_section:
                            string_section = string_section.replace('#------------------------------', '')

                        new_string_sections[index] = string_section


                    path = plugin_sub_template_dir[name]['path']

                    if extension_type != 'Property':
                        with open(os.path.join(path, f'{name}Setup.py'), 'w') as f:
                            f.write(new_string_sections[0])

                        with open(os.path.join(path, f'{name}Layout.py'), 'w') as f:
                            f.write(new_string_sections[1])
                    else:
                        with open(os.path.join(path, f'{name}Property.py'), 'w') as f:
                            f.write(new_string_sections[2])


        uiplugin_name = f'{self._plugin_name.text()}.uiplugin'

        if 'None' in plugin_sub_categories:
            plugin_sub_categories.pop('None')

        categories_setup = []
        for category in plugin_sub_categories:
            new_category = {'Name': category}

            for item in plugin_sub_categories[category]:

                if 'Modules' not in new_category:
                    new_category['Modules'] = []

                new_category['Modules'].append(item['Module_Path'])

            categories_setup.append(new_category)

        uiplugin_file_data = {
            "Icons": f'{"IconRegistration" if not self._enable_icon.isChecked() else ""}',
            "Properties": properties,
            "Categories": categories_setup
        }

        with open(os.path.join(plugin_dir, uiplugin_name), 'w') as file:
            json.dump(uiplugin_file_data,file, indent=4)

        data = SetupTools.tool_Json_data()[0]
        path = SetupTools.tool_Json_data()[1]

        data['Plugins'].append({'Name': self._plugin_name.text(), 'Enable': True})
        index = len(data['Plugins']) - 1
        WindowsModule.WindowsManger.add_plugin(self._plugin_name.text(), data['Plugins'][index]['Enable'], plugin_dir)

        SetupTools.load_plugin_modules(self._plugin_name.text(), plugin_dir, SetupTools.LOAD_MODULE)

        with open(path, 'w') as file:
            json.dump(data, file, indent=4)

        self._parent.update_plugin_list()
        self.close()
        self._parent._parent._plugin_create_win = None



class plugin_tab_widget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(plugin_tab_widget, self).__init__(parent)
        self._parent = parent

        self._item_name = QtWidgets.QLineEdit()
        self._category = QtWidgets.QLineEdit()
        self._type = QtWidgets.QComboBox()

        self._item_name.setToolTip('Enter a name')
        self._category.setToolTip('Enter a category')

        self._type.addItems(['Parameter', 'Folder', 'Property'])

        self._tab_widget_layout = QtWidgets.QFormLayout()
        self._tab_widget_layout.setAlignment(QtCore.Qt.AlignTop)

        self._tab_widget_layout.addRow('Name : ', self._item_name)
        self._tab_widget_layout.addRow('Category : ', self._category)
        self._tab_widget_layout.addRow('Type : ', self._type)
        self._tab_widget_layout.addWidget(SeparatorWidgetClass.SeparatorHWidget())

        self.setLayout(self._tab_widget_layout)

        self._item_name.textChanged.connect(self.check_name)
        self._type.currentTextChanged.connect(self.type_update)


    def clone(self, parent=None, layout=None, state: bool = False):
        clone_widget = plugin_tab_widget(self._parent)
        self._parent.update_date(clone_widget)
        return clone_widget

    def check_name(self):
        new_name = StringValidatorClass.checkString(self._item_name.text())
        self._item_name.setText(new_name)

    def type_update(self, arg):
        if arg == 'Property':
            self._category.setEnabled(False)
        else:
            self._category.setEnabled(True)

    def get_name_widget(self):
        return self._item_name

    def get_category_widget(self):
        return self._category

    def get_name(self):
        return self._item_name.text()

    def get_category(self):
        return self._category.text()

    def get_type(self):
        return self._type.currentText()