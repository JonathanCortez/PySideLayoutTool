import os
import re
from typing import List, Dict, Any
from PySide2 import QtWidgets

from PySideLayoutTool.UIEditorLib import UIEditorFactory, TreeItemInterface, RootWidget, UIFunctions as ui
from PySideLayoutTool.UIEditorTemplates.Layout import CustomFormLayout
import pickle


class TemplateData:

    def __init__(self, parent):
        self._parent = parent

        self._layout_names: Dict[Any,str] = {}
        self._widget_groups: Dict[str, List[Any]] = {}
        self._item_groups: Dict[str, List[Any]] = {}
        self._folderlist_groups: Dict[str, str] = {}

        self._layout_widgets: Dict[str, Any] = {}

        self._string_groups: Dict[str, List[str]] = {}
        self._display_groups: Dict[str, List[Any]] = {}

    def layout_names(self):
        return self._layout_names

    def widget_groups(self):
        return self._widget_groups

    def item_groups(self):
        return self._item_groups

    def display_groups(self):
        return self._display_groups

    def string_groups(self):
        return self._string_groups

    def find_widget(self, name):
        if name in self._layout_widgets:
            return self._layout_widgets[name]

        else:
            return None

    def clear_data(self):
        self._layout_names.clear()
        self._widget_groups.clear()
        self._item_groups.clear()
        self._display_groups.clear()
        self._layout_widgets.clear()
        self._folderlist_groups.clear()

    def remove_data_obj(self, current_item, full_remove=True):
        name_find = current_item.itemParent().name()
        name_str = self._layout_names.pop(current_item)
        index = -1
        for i in enumerate(self._item_groups[name_find]):
            if i[1] is current_item:
                index = i[0]
                break

        if current_item.name() in self._folderlist_groups:
            self._folderlist_groups.pop(current_item.name())

        if current_item.name() in self._layout_widgets:
            self._layout_widgets.pop(current_item.name())

        if current_item.name() in self._widget_groups:
            if len(self._widget_groups[current_item.name()]) > 0 and full_remove:
                self.move_data_groups(self._widget_groups, name_find, current_item.name())
                self.move_data_groups(self._item_groups, name_find, current_item.name())
                self.move_data_groups(self._display_groups, name_find, current_item.name())
                self.move_data_groups(self._string_groups, name_find, current_item.name())

            del self._widget_groups[current_item.name()]
            del self._item_groups[current_item.name()]
            del self._display_groups[current_item.name()]
            del self._string_groups[current_item.name()]

        item = self._item_groups[name_find].pop(index)
        widget = self._widget_groups[name_find].pop(index)
        display = self._display_groups[name_find].pop(index)
        type = self._string_groups[name_find].pop(index)
        del name_str, item, widget, display, type


    def move_data_groups(self, data, name_move_to, current_name):
        for group_item in data[current_name]:
            data[name_move_to].append(group_item)


    def find_group_item(self, item):
        last_index = -1
        last_key = None

        for key in self._item_groups:
            for index, i in enumerate(self._item_groups[key]):
                if item is i:
                    return index, key

        return last_index, last_key

    def find_group_widget(self, name : str):
        index = -1
        key_in = None
        for key in self._widget_groups:
            for n, item in enumerate(self._widget_groups[key]):
                if item.name() == name:
                    index = n
                    key_in = key
                    break

        return index, key_in


    def update_names(self, item, new_name: str):
        name = self._layout_names.pop(item)
        self._layout_names[item] = new_name

        if name in self._widget_groups:
            current_list = self._widget_groups.pop(name)
            self._widget_groups[new_name] = current_list
            current_list = self._item_groups.pop(name)
            self._item_groups[new_name] = current_list
            current_list = self._string_groups.pop(name)
            self._string_groups[new_name] = current_list
            current_list = self._display_groups.pop(name)
            self._display_groups[new_name] = current_list

            current_widget = self._layout_widgets.pop(name)
            self._layout_widgets[new_name] = current_widget

        if name in self._folderlist_groups:
            current_widget = self._folderlist_groups.pop(name)
            self._folderlist_groups[new_name] = current_widget


    def add_group_data(self, item, widget, display, type_str, index: int):
        name = item.itemParent().name()
        if name not in self._widget_groups:
            self._widget_groups[name] = [widget]
            self._item_groups[name] = [item]
            self._string_groups[name] = [type_str]
            self._display_groups[name] = [display]

        else:
            current_widget_list = self._widget_groups[name]
            current_widget_list.insert(index,widget)
            self._widget_groups[name] = current_widget_list

            current_item_list = self._item_groups[name]
            current_item_list.insert(index, item)
            self._item_groups[name] = current_item_list

            current_display_list = self._display_groups[name]
            current_display_list.insert(index, display)
            self._display_groups[name] = current_display_list

            current_string_list = self._string_groups[name]
            current_string_list.insert(index, type_str)
            self._string_groups[name] = current_string_list

        self._layout_widgets[item.name()] = widget


    def add_folderlist_data(self,base_name, widget, above_item_name):
        if not self._folderlist_groups:
            self._folderlist_groups[base_name] = widget

        else:
            if above_item_name in self._folderlist_groups:
                parent_widget = self._folderlist_groups[above_item_name]
                self._folderlist_groups[base_name] = parent_widget

            else:
                self._folderlist_groups[base_name] = widget


    def update_groups(self, item, new_index:int):
        name = item.itemParent().name()
        last_index, last_key = self.find_group_item(item)

        self._item_groups[last_key].pop(last_index)
        widget = self._widget_groups[last_key].pop(last_index)
        type = self._string_groups[last_key].pop(last_index)
        display = self._display_groups[last_key].pop(last_index)
        
        if name not in self._item_groups:
            self.add_group_data(item,widget,display, type, new_index)
        else:
            self._item_groups[name].insert(new_index, item)
            self._widget_groups[name].insert(new_index, widget)
            self._display_groups[name].insert (new_index,display)
            self._string_groups[name].insert(new_index, type)


    def newLayout(self, main_layout_win) -> 'TemplateGroup':
        current_layout = TemplateGroup()
        current_layout.setData(self)
        current_layout.setTemplateName('Root')
        main_layout_win._widgets.clear()

        if 'Root' in self._widget_groups:
            self.recursiveLayout(main_layout_win, 'Root', current_layout, self._widget_groups)
        else:
            current_layout._mainLayout.add_Custom(RootWidget.RootWidget())

        return current_layout


    def cloneLayout(self,parent_widget, parent_layout, name: str, pre_def_dict, new_name=None):
        new_widget_group: Dict[str, List[Any]] = pre_def_dict

        for index, widget_type in enumerate(self._string_groups[name]):
            widget = self._widget_groups[name][index]
            build_class = UIEditorFactory.WidgetFactory.create(widget_type)
            build_class.clone_widget(parent_layout, parent_widget, widget)

            if new_name:
                if new_name not in new_widget_group:
                    new_widget_group[new_name] = [build_class.newWidget()]
                else:
                    new_widget_group[new_name].append(build_class.newWidget())
            else:
                if name not in new_widget_group:
                    new_widget_group[name] = [build_class.newWidget()]
                else:
                    new_widget_group[name].append(build_class.newWidget())

            if widget.name() in self._widget_groups:
                new_widget_group = self.cloneLayout(widget.name(), new_widget_group, getattr(build_class.newWidget(), '__property_instances__')['name'].value())

        return new_widget_group


    def recursiveLayout(self, main_layout_win,  name:str, template_layout, widget_data, update_clear = True):
        for widget_update in widget_data[name]:
            widget_update._updateProperties()
            widget_update.clear_Observers()

        # index = start_index

        for index,widget in enumerate(widget_data[name]):
            widget.PreUpdate()
            self._process_script(widget.callback(), widget)

            if name in self._item_groups:
                if isinstance(self._item_groups[name][index], TreeItemInterface.FolderItem):
                    if widget.name() not in widget_data:
                        self.final_process(widget)
                        self.add_widget_to_layout_data(main_layout_win, widget)
                        continue

            #Folder
            if widget.name() in widget_data:
                if update_clear:
                    widget.clearLayout()

                # if child:
                #     widget.parent_id = self.find_widget(name).widget_id
                #
                # widget.is_child = child
                # widget.widget_id = index

                # index += 1
                widget.templateGroup().setData(self)
                widget.templateGroup().setTemplateName(widget.name())
                self.recursiveLayout(main_layout_win, widget.name(), widget.templateGroup(), widget_data)

                if 'Multiparm'.find(widget.type().currentItem_name):
                    for name in widget.templateGroup().templateGroupData():
                        main_layout_win.widget_layout().pop(name)

                #Folder List
                if widget.name() in self._folderlist_groups:
                    parent_widget = self._folderlist_groups[widget.name()]
                    if parent_widget == widget or widget.endGroup():
                        widget.setParentTab(True)
                        template_layout.addChild_noLabel(widget)
                    else:
                        parent_widget._folder_widget.newTab(widget.templateGroup(), widget.label()) #type: ignore

                else:
                    template_layout.addChild_noLabel(widget)

            #Parameters
            else:
                # if child:
                #     widget.parent_id = self.find_widget(name).widget_id
                #
                # widget.is_child = child
                # widget.widget_id = index
                if hasattr(widget, 'bNeighbor'):
                    template_layout.horizontal_join(widget)

            # index += 1
            self.final_process(widget)
            self.add_widget_to_layout_data(main_layout_win, widget)


    def final_process(self, widget):
        widget.PostUpdate()
        widget._setHidden_expression(self._conditionHandle(widget.hiden_when(), widget))
        widget._setDisable_expression(self._conditionHandle(widget.disable_when(), widget))

        if widget.invisible():
            widget._hidden_implementation(widget.invisible())


    def add_widget_to_layout_data(self, layout_win, widget):
        layout_win.widget_layout()[widget.name()] = widget


    def _conditionHandle(self, expression: str, widget_on):
        if expression != '':
            exp_list = self._expression_format([i.split() for i in re.findall("{(.*?)}", expression)], widget_on)
            return None if exp_list == [] else exp_list

        return None


    def _expression_format(self, string_list: List[str], widget_on):
        expressionList = []
        string_lenght = len(string_list)

        for num in range(0, string_lenght,1):
            current_str_list_len = len(string_list[num])
            count = 0
            for str_item in enumerate(string_list[num]):
                count += 1
                index, key_in = self.find_group_widget(str_item[1])
                if index != -1:
                    base_observer = self._widget_groups[key_in][index]
                    if base_observer != widget_on:
                        base_observer.add_Observer(widget_on)
                        expressionList.append(base_observer)
                    else:
                        expressionList.append('None')
                else:
                    expressionList.append(str_item[1])

                if count == 3 and str_item[0] != current_str_list_len-1:
                    expressionList.append('and')
                    count = 0

            if num != string_lenght-1:
                expressionList.append('or')

        return expressionList


    def _process_script(self, expression: str, widget_obj):
        if expression != '':
            split_expression = expression.split('.')

            if split_expression[0] == 'ui':
                expression_path = '.'.join(split_expression[:3])
                call = '.'.join(split_expression[3:])
                args = call[call.find("(")+1:call.find(")")]

                if args:
                    new_args = {}
                    if "kwargs['layout']" in args:
                        new_args['layout'] = widget_obj._parent
                    if "kwargs['parm']" in args:
                        new_args['parm'] = widget_obj

                    args = new_args

                expression = compile(expression_path, 'Script', 'eval')
                code = eval(expression)

                if code:
                    setattr(widget_obj, '__code_obj__', code)
                    setattr(widget_obj, '__call_obj__', call)
                    if args:
                        setattr(widget_obj,'__call_args__', args)
            else:
                pass



class TemplateGroup(QtWidgets.QWidget):

    def __init__(self):
        super(TemplateGroup, self).__init__()
        self._template_layout_data: Dict[str,Any] = {}

        self._parent_layout_item = None
        self.__data_class = None
        self._template_name = None

        self._mainLayout = CustomFormLayout.CustomForm()
        self.setLayout(self._mainLayout)


    def addChild(self, widget: QtWidgets.QWidget, apply_layout=True):
        layout_item = self._mainLayout.new_Row(widget.label(),widget.name(), widget, apply_to_main=apply_layout)
        self._template_layout_data[widget.name()] = widget
        widget.set_layout_parent(layout_item)
        return layout_item


    def addChild_noLabel(self,widget: QtWidgets.QWidget):
        self._mainLayout.add_Custom(widget)
        self._template_layout_data[widget.name()] = widget


    def horizontal_join(self, widget):
        if widget.bNeighbor() and self._parent_layout_item is None:
            self._parent_layout_item = QtWidgets.QHBoxLayout()
            self._parent_layout_item.setContentsMargins(0, 0, 0, 0)
            self._parent_layout_item.setSpacing(10)
            item = self.addChild(widget, False)
            self._parent_layout_item.addLayout(item)

        else:
            if self._parent_layout_item:
                if widget.bLabel():
                    item = self.addChild(widget, False)
                    self._parent_layout_item.addLayout(item)
                    widget.set_label_widget(self._mainLayout.labels(widget))
                else:
                    self._parent_layout_item.addWidget(widget)

                if not widget.bNeighbor():
                    self._mainLayout.add_Layout(self._parent_layout_item)
                    self._parent_layout_item = None
            else:
                if widget.bLabel():
                    self.addChild(widget)
                    widget.set_label_widget(self._mainLayout.labels(widget))
                else:
                    self.addChild_noLabel(widget)

        widget.set_layout_parent(self._mainLayout)


    def templateGroupData(self):
        return self._template_layout_data

    def find_widget_id(self, id: int):
        for key in self._template_layout_data:
            if self._template_layout_data[key].widget_id == id:
                return self._template_layout_data[key]

        return None

    def find_widget(self,name: str) -> Any or None:
        if name in self._template_layout_data:
            return self._template_layout_data[name]

        return None

    def setTemplateName(self, name: str):
        self._template_name = name

    def setData(self,data_class):
        self.__data_class = data_class

    def clone(self,parent, layout_win, state: bool):
        clone_template = TemplateGroup()
        clone_template.setTemplateName(self._template_name)
        clone_template.setData(self.__data_class)
        new_clone_widgets = self.__data_class.cloneLayout(parent, layout_win, self._template_name, {})
        self.__data_class.recursiveLayout(layout_win , self._template_name, clone_template, new_clone_widgets, state)
        return clone_template




#TODO : REDO Template Serialization to public class not instance.
class TemplateSerialization:

    def __init__(self, path, data_base):
        self._current_data_base = data_base
        self._path = path
        self._built_data = {}

    def write_commonData(self):
        self._built_data['Types'] = self._current_data_base.string_groups()

        property_groups: Dict[str, List[Dict[str, Any]]] = {}
        value_list : Dict[str, List[str]] = {}
        for key_display in self._current_data_base.display_groups():
            property_list = []
            widget_values = []
            for i in self._current_data_base.display_groups()[key_display]:
                property_dict = {}
                for widget_property in i.Properties():
                    property_dict[widget_property] = i.Properties()[widget_property].value() if i.Properties()[widget_property].value() else 'None'

                property_list.append(property_dict)

            for w in self._current_data_base.widget_groups()[key_display]:
                widget_values.append(str(w.eval()))

            property_groups[key_display] = property_list
            value_list[key_display] = widget_values

        self._built_data['Type_Properties'] = property_groups
        self._built_data['Values'] = value_list

        if self._current_data_base._parent.pyModules() > 0:
            py_editor = self._current_data_base._parent.pyEditor().pyModule_editor()
            py_modules : Dict[str, str] = {}
            for module_name in py_editor.modules().keys():
                code_str = self._current_data_base._parent.pyModule(module_name)
                py_modules[module_name] = code_str

            self._built_data['Py_Modules'] = py_modules

    def writeData(self,key_name: str, value_data: Any):
        self._built_data[key_name] = value_data

    def saveData(self, force_save=False):
        if not os.path.exists(self._path) or force_save:
            with open(self._path, 'wb') as currentFile:
                pickle.dump(self._built_data, currentFile, protocol=pickle.HIGHEST_PROTOCOL)


