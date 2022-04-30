import ast
import json
from PySide2 import QtWidgets

class JsonConstructor:

    _folder_types = ['Simple','Collapisble']
    _folderlist_types = ['Tabs','Radio']

    @classmethod
    def construct(cls, file, editor_win):
        editor_tree = editor_win.parameter_Tab().layout_tree()
        data = json.load(file)

        for item in data['Root']:
            if item['Type'] in cls._folderlist_types:
                for folder in item['Folders']:
                    folder_build = editor_tree.add_new_obj(folder['Type'], editor_tree.root_item(),QtWidgets.QAbstractItemView.OnItem)
                    folder_display_widget = folder_build.newDisplay()
                    folder_item = folder_build.newItem()
                    editor_tree.setExpanded(editor_tree.indexFromItem(folder_item), True)

                    for property_name in folder_display_widget.Properties():
                        if property_name in folder:
                            if property_name != 'Type':
                                folder_display_widget.Properties()[property_name].setValue(folder[property_name])
                            if property_name == 'Name':
                                folder_display_widget.mediatorNameCheck()
                            elif property_name == 'Label':
                                folder_display_widget.mediatorLabel()

                    for parameter in folder['FolderParameters']:
                        parm_build = editor_tree.add_new_obj(parameter['Type'], folder_item ,QtWidgets.QAbstractItemView.OnItem)
                        parm_display_widget = parm_build.newDisplay()

                        for property_name in parm_display_widget.Properties():
                            if property_name in parameter:
                                if property_name != 'Type':
                                    current_value = ''
                                    if property_name == 'Values':
                                        if parameter['Type'] != 'Ramp':
                                            current_value = ast.literal_eval(parameter['Settings']['Values'])
                                    else:
                                        current_value = parameter[property_name]
                                    parm_display_widget.Properties()[property_name].setValue(current_value)
                                if property_name == 'Name':
                                    parm_display_widget.mediatorNameCheck()
                                elif property_name == 'Label':
                                    parm_display_widget.mediatorLabel()

                        if parameter['Type'] == 'Ramp':
                            parm_build.newWidget().set_value(parameter['Settings']['Values'])


            elif item['Type'] in cls._folder_types:
                folder_build = editor_tree.add_new_obj(item['Type'], editor_tree.root_item(),QtWidgets.QAbstractItemView.OnItem)
                folder_display_widget = folder_build.newDisplay()
                folder_item = folder_build.newItem()
                editor_tree.setExpanded(editor_tree.indexFromItem(folder_item), True)


                for property_name in folder_display_widget.Properties():
                    if property_name in item:
                        if property_name != 'Type':
                            folder_display_widget.Properties()[property_name].setValue(item[property_name])
                        if property_name == 'Name':
                            folder_display_widget.mediatorNameCheck()
                        elif property_name == 'Label':
                            folder_display_widget.mediatorLabel()


                for parameter in item['FolderParameters']:
                    parm_build = editor_tree.add_new_obj(parameter['Type'], folder_item,QtWidgets.QAbstractItemView.OnItem)
                    parm_display_widget = parm_build.newDisplay()

                    for property_name in parm_display_widget.Properties():
                        if property_name in parameter:
                            if property_name != 'Type':
                                current_value = ''
                                if property_name == 'Values':
                                    if parameter['Type'] != 'Ramp':
                                        current_value = ast.literal_eval(parameter['Settings']['Values'])
                                else:
                                    current_value = parameter[property_name]
                                parm_display_widget.Properties()[property_name].setValue(current_value)
                            if property_name == 'Name':
                                parm_display_widget.mediatorNameCheck()
                            elif property_name == 'Label':
                                parm_display_widget.mediatorLabel()

                    if parameter['Type'] == 'Ramp':
                        parm_build.newWidget().set_value(parameter['Settings']['Values'])

            else:
                parm_build = editor_tree.add_new_obj(item['Type'], editor_tree.root_item(),QtWidgets.QAbstractItemView.OnItem)
                parm_display_widget = parm_build.newDisplay()

                for property_name in parm_display_widget.Properties():
                    if property_name in item or property_name == 'Values':
                        if property_name != 'Type':
                            current_value = ''
                            if property_name == 'Values':
                                if item['Type'] != 'Ramp':
                                    current_value = ast.literal_eval(item['Settings']['Values'])
                            else:
                                current_value = item[property_name]
                            parm_display_widget.Properties()[property_name].setValue(current_value)
                        if property_name == 'Name':
                            parm_display_widget.mediatorNameCheck()
                        elif property_name == 'Label':
                            parm_display_widget.mediatorLabel()

                if item['Type'] == 'Ramp':
                    parm_build.newWidget().set_value(item['Settings']['Values'])

        editor_tree.setExpanded(editor_tree.indexFromItem(editor_tree.root_item()), True)
