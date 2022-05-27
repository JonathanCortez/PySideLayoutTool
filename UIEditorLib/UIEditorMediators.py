from abc import abstractmethod, ABC
from typing import Any
from enum import Enum
from . import TemplateDataClass, UIEditorFactory

from PySide2 import QtWidgets

class NotifyType(Enum):
    notifyLabel = 1
    notifyCheckNames = 2


class Mediator(ABC):

    @abstractmethod
    def notify(self, sender: Any, notify_arg: NotifyType , **kwargs) -> None:
        """

        :param sender:
        :param notify_arg:
        :param kwargs:
        """

    @abstractmethod
    def notifyAll(self,**kwargs):
        pass


# TODO: Note: This Class/Module must be better exam to implement a S.O.L.I.D Principle so others can extend without breaking everything else



class LayoutMediator(Mediator):
    def __init__(self, itemComp, viewComp) -> None:
        self._item_component = itemComp
        self._item_component.mediator = self
        self._view_component = viewComp
        self._view_component.mediator = self


    # def funcType(self, type_index: int):
    #     return {
    #         1: self.updateLabels,
    #         2: self.checkNames
    #     }[type_index]


    def update_item_name(self, name:str):
        self._item_component.setName(name)

    def notify_item_label(self, new_label: str):
        self._item_component.setLabel(new_label)

    def notify_display_label(self, new_label:str):
        widget, label_widget = self._view_component.findProperty('Label')
        widget.setText(new_label)

    def updateChange(self, type_string: str):
        base_tree = self._item_component.treeWidget()
        index = base_tree.EditorWin().TemplateLayout().find_group_item(self._item_component)

        items = []
        if self._item_component.childCount() > 0:
            for i in base_tree.EditorWin().TemplateLayout().item_groups()[self._item_component.name()]:
                self._item_component.removeChild(i)
                items.append(i)

        display_widget = base_tree.displayObject().widgetStack(self._item_component.stackIndex)
        base_tree.displayObject().removeStack(display_widget)
        base_tree._update_display_item_index()
        self._item_component.itemParent().removeChild(self._item_component)
        base_tree.EditorWin().TemplateLayout().remove_data_obj(self._item_component)
        del display_widget

        category = UIEditorFactory.WidgetFactory.ItemCategoryIn(type_string)

        builder = UIEditorFactory.WidgetFactory.create(type_string)
        builder.InitObjects()
        builder.FillObjects(category, type_string)
        builder.Item_management_index(self._item_component, index[0])
        builder.Database_Fill(base_tree)

        if len(items) > 0:
            for i in enumerate(items):
                i[1].setItem(builder.newItem())
                builder.newItem().itemHandling(i[1], QtWidgets.QAbstractItemView.OnItem)
                base_tree.EditorWin().TemplateLayout().update_groups(i[1], i[0])

            base_tree.setExpanded(base_tree.indexFromItem(builder.newItem()), True)

        base_tree._check_below_items()



    #TODO: Change verifyName to checkNames but on another subclass of this class
    def verifyName(self, name_check: str, ) -> str:
        new_name = self.checkNames(name_check, False)
        self._item_component.treeWidget().EditorWin().TemplateLayout().update_names(self._item_component, new_name)
        return new_name


    def checkNames(self, name: str, new : bool) -> str:
        if name in self.added_names().values():
            if 2 <= list(self.added_names().values()).count(name) or new:
                str_lenght = len(name)-1
                if name[str_lenght].isdigit():
                    str_num = str(int(name[str_lenght]) + 1)
                    name = name.replace(name[str_lenght], str_num)
                else:
                    name += '1'

                return self.checkNames(name, True)

        return name


    def added_names(self):
        return self._item_component.treeWidget().EditorWin().TemplateLayout().layout_names()


    def notify(self, sender: Any, notify_arg: NotifyType , **kwargs) -> None:
        pass
        # instance_vars = vars(self)
        # instance_vars = list(instance_vars.values())
        # for comp in instance_vars:
        #     if comp is not sender:
        #         self.funcType(notify_arg.value)(component=comp, **kwargs)     #type: ignore


    def notifyAll(self,**kwargs):
        name = self.checkNames(kwargs['name'], True)
        label = kwargs['label']
        self._item_component.setName(name)
        self._item_component.setLabel(label)
        widget, label_widget = self._view_component.findProperty('Name')
        widget.setText(name)




class EditorsMediator(Mediator):

    def __init__(self, editor_window, layout_window):
        self._mainEditor = editor_window
        self._mainEditor.mediator = self
        self._layoutWin = layout_window
        # self._layoutWin.mediator = self
        self._serialization = TemplateDataClass.TemplateSerialization(self._mainEditor.editor_path(), self._mainEditor.TemplateLayout())
        self._layoutWin._serialization_obj = self._serialization

        self._prev_item = None

    def notifyUpdate(self,widget: QtWidgets.QWidget):
        self._layoutWin.UpdateLayout(widget)
        self._serialization.write_commonData()
        self._serialization.saveData(force_save=True)

    def notify_force_update(self):
        self._serialization.write_commonData()
        self._serialization.saveData(force_save=True)

    def notify_full_serialization(self):
        self._serialization.writeData('Name', self._mainEditor.editor_name())
        self._serialization.writeData('Category', self._mainEditor.editor_category())
        self._serialization.saveData()

    def notify_save(self):
        self._serialization.saveData()

    def notifyDisplay(self):
        self._layoutWin.display()

    def layout_window(self):
        return self._layoutWin

    def restoreWins(self, data):
        if 'Types' in data:
            editor_tree = self._mainEditor.parameter_Tab().layout_tree()
            for index , parm_type in enumerate(data['Types']['Root']):
                self._prev_item = editor_tree.root_item()
                self._recursive_build(parm_type,'Root', index, data, editor_tree)


        if 'Py_Modules' in data:
            py_editor = self._mainEditor.pyEditor().pyModule_editor()
            modules_data = data['Py_Modules']

            for index, py_name in enumerate(modules_data.keys()):
                py_editor.newTabCode(index, py_name, modules_data[py_name])

        self._layoutWin.UpdateLayout(self._mainEditor.TemplateLayout().newLayout(self._layoutWin))


    def _lastCheck(self, name, display):
        if name == 'Name':
            display.mediatorNameCheck()
        elif name == 'Label':
            display.mediatorLabel()

    def _rebuild_state(self,type_string, key_in, index: int, item_on, data, tree):
        builder = tree.add_new_obj(type_string, item_on, QtWidgets.QAbstractItemView.OnItem)
        self._prev_item = builder.newItem()
        
        property_data = data['Type_Properties'][key_in][index]
        for property_name in property_data:
            display_obj = builder.newDisplay()
            widget_property, label_widget = display_obj.findProperty(property_name)
            widget_property.setValue(property_data[property_name])
            self._lastCheck(property_name, display_obj)

        if 'Default' in property_data:
            if not property_data['Default']:
                if data['Values'][key_in][index] != property_data['Default']:
                    builder.newWidget().set_value(data['Values'][key_in][index])

        return builder

    def _recursive_build(self, parm_string: str ,key_name: str, index_on, data, tree):
        item_on = self._prev_item if self._prev_item.bOnItem() else self._prev_item.itemParent()
        builder = self._rebuild_state(parm_string ,key_name, index_on, item_on, data, tree)

        if builder.newItem().bOnItem():
            item_name = builder.newItem().name()
            if item_name in data['Types']:
                for index,folder_type in enumerate(data['Types'][item_name]):
                    self._recursive_build(folder_type,item_name, index, data, tree)

        tree.setExpanded(tree.indexFromItem(item_on), True)

    def notify(self, sender: Any, notify_arg: NotifyType, **kwargs) -> None:
        pass

    def notifyAll(self, **kwargs):
        pass





class MainEditorMediator(Mediator):

    def __init__(self, main_window, tree_widget, process_widget):
        self._main_window = main_window
        self._main_window.mediator = self
        self._tree_layout = tree_widget
        self._tree_layout.mediator = self
        self._process_widget = process_widget
        self._process_widget.mediator = self

    @staticmethod
    class NotifyType(Enum):
        notifyNew = 0
        notifyArrange = 1
        notifyRemove = 2

    def funcType(self, type_index: int):
        return {
            0: self.newTemplate,
            1: self.ArrangeGroup,
            2: self.removeTemplate
        }[type_index]

    def newTemplate(self, widget, itemOn):
        self._process_widget.newTemplateAdd(widget, itemOn)

    def ArrangeGroup(self, index):
        pass

    def removeTemplate(self, **kwargs):
        pass

    def displayLayout(self):
        self._main_window.mediatorEditor.notifyDisplay()

    def LayoutUpdate(self, widget: QtWidgets.QWidget):
        self._main_window.mediatorEditor.notifyUpdate(widget)

    def notify(self, sender: Any, notify_arg: NotifyType, **kwargs) -> None:
        pass

    def notifyAll(self, **kwargs):
        pass



class BaseComponent:
    """
    The Base Component provides the basic functionality of storing a mediator's
    instance inside component objects.
    """

    def __init__(self, mediator: Mediator = None) -> None:
        self._mediator = mediator

    @property
    def mediator(self) -> Mediator:
        return self._mediator

    @mediator.setter
    def mediator(self, mediator: Mediator) -> None:
        self._mediator = mediator